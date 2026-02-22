# Indexer Setup Guide

## Overview

Midnight Indexer indexes blockchain data into a database for efficient querying via GraphQL API.

## ⚠️ Version Information

### Current Version (RECOMMENDED)
- **v3.0.0** (Released: January 28, 2026)
  - Updated Indexer API to v3 only
  - Support for Ledger v7 and Node v0.20 only
  - Support for unshielded tokens
  - Docker images: `midnightntwrk/indexer-api`
  - **Breaking changes from v2.x**

### Deprecated Versions (DO NOT USE)
- **v2.1.4**: UNSUPPORTED - Use v3.0.0
- **v2.1.0-2.1.3**: DEPRECATED
- **v2.0.0**: DEPRECATED

### Migration Required
If running v2.x, migrate to v3.0.0 immediately. See [Migration Guide](#migration-from-v2x-to-v30) below.

## Requirements

### Compatibility
- **Node**: v0.20 or higher
- **Ledger**: v7 or higher
- **Indexer API**: v3 only

### Hardware
- CPU: 4+ cores
- RAM: 8GB+ (16GB recommended)
- Storage: 1TB+ SSD
- Network: 100Mbps+

### Software
- Docker (recommended) or PostgreSQL 13+
- Midnight Node v0.20+

## Installation

### Docker Deployment (Recommended)

#### 1. Pull Docker Image
```bash
docker pull midnightntwrk/indexer-api:3.0.0
```

#### 2. Configure PostgreSQL
```bash
docker run -d \
  --name midnight-postgres \
  -e POSTGRES_DB=midnight_indexer \
  -e POSTGRES_USER=indexer \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  postgres:13
```

#### 3. Run Indexer
```bash
docker run -d \
  --name midnight-indexer \
  --link midnight-postgres:postgres \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://indexer:secure_password@postgres:5432/midnight_indexer \
  -e NODE_RPC_URL=http://midnight-node:9933 \
  -e NODE_WS_URL=ws://midnight-node:9944 \
  midnightntwrk/indexer-api:3.0.0
```

### Manual Installation (Advanced)

#### 1. Install PostgreSQL
```bash
sudo apt install postgresql-13
sudo systemctl start postgresql
```

#### 2. Create Database
```sql
CREATE DATABASE midnight_indexer;
CREATE USER indexer WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE midnight_indexer TO indexer;
```

#### 3. Download Indexer v3.0.0
```bash
# Check releases page for latest v3.0.0 binary
# https://docs.midnight.network/relnotes/midnight-indexer/
wget https://releases.midnight.network/indexer-3.0.0.tar.gz
tar -xzf indexer-3.0.0.tar.gz
cd midnight-indexer
```

#### 4. Configure
Edit `indexer-config.yaml`:
```yaml
database:
  host: localhost
  port: 5432
  name: midnight_indexer
  user: indexer
  password: secure_password

node:
  rpc_url: http://localhost:9933
  ws_url: ws://localhost:9944

indexing:
  start_block: 0
  batch_size: 100
```

#### 5. Run Migrations
```bash
./midnight-indexer migrate --config indexer-config.yaml
```

#### 6. Start Indexer
```bash
./midnight-indexer start --config indexer-config.yaml
```

## GraphQL API

Indexer exposes GraphQL API v3 on port 3000:
```
http://localhost:3000/graphql
```

### API v3 Features
- Unshielded token support
- Enhanced query performance
- Real-time subscriptions
- Ledger v7 compatibility

### Example Queries
```graphql
query {
  latestBlock {
    number
    timestamp
    transactions {
      hash
      status
    }
  }
}
```

## Monitoring

### Check Sync Status
```bash
curl http://localhost:3000/health
```

### Database Size
```sql
SELECT pg_size_pretty(pg_database_size('midnight_indexer'));
```

## Maintenance

### Vacuum Database
```sql
VACUUM ANALYZE;
```

### Reindex
```bash
./midnight-indexer reindex --from-block 0
```

## Performance Tuning

### PostgreSQL
```sql
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
```

### Indexer
- Increase `batch_size` for faster sync
- Use SSD for database
- Optimize queries with indexes

## Migration from v2.x to v3.0

### Breaking Changes
- API v3 only (v2 endpoints removed)
- Requires Node v0.20+ and Ledger v7+
- Database schema changes
- New unshielded token tables

### Migration Steps

#### 1. Backup Existing Data
```bash
pg_dump midnight_indexer > indexer_v2_backup.sql
```

#### 2. Stop v2.x Indexer
```bash
./midnight-indexer stop
# or
docker stop midnight-indexer
```

#### 3. Update Database Schema
```bash
# With v3.0.0 binary
./midnight-indexer migrate --config indexer-config.yaml
```

#### 4. Deploy v3.0.0
Follow [Docker Deployment](#docker-deployment-recommended) instructions above.

#### 5. Verify Migration
```bash
curl http://localhost:3000/health
# Should return: {"status":"ok","version":"3.0.0"}
```

### Rollback (If Needed)
```bash
# Restore v2.x database
psql midnight_indexer < indexer_v2_backup.sql

# Redeploy v2.x indexer (not recommended)
```

## Troubleshooting

### Version Mismatch Errors
```
Error: Indexer API v3 requires Node v0.20+
```
**Solution**: Upgrade Midnight Node to v0.20 or higher.

### Database Migration Fails
```
Error: Schema migration failed
```
**Solution**: Backup data, drop database, recreate, run migrations.

### Unshielded Token Queries Fail
```
Error: Unshielded token support requires Ledger v7
```
**Solution**: Ensure Node is running Ledger v7+.

## Resources

- Release Notes: https://docs.midnight.network/relnotes/midnight-indexer/midnight-indexer-3-0-0
- Docker Hub: https://hub.docker.com/r/midnightntwrk/indexer-api
- GraphQL Schema: http://localhost:3000/graphql (when running)
- Compatibility Matrix: https://docs.midnight.network/relnotes/support-matrix
