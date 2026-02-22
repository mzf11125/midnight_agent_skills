# Indexer Setup Guide

## Overview

Midnight Indexer indexes blockchain data into a database for efficient querying.

## Versions

- **v2.0.0**: Initial release
- **v2.1.0**: Performance improvements
- **v2.1.4**: Latest stable (recommended)

## Requirements

### Hardware
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 1TB+ SSD
- Network: 100Mbps+

### Software
- PostgreSQL 13+
- Midnight Indexer binary
- Midnight Node (for data source)

## Installation

### 1. Install PostgreSQL
```bash
sudo apt install postgresql-13
sudo systemctl start postgresql
```

### 2. Create Database
```sql
CREATE DATABASE midnight_indexer;
CREATE USER indexer WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE midnight_indexer TO indexer;
```

### 3. Install Indexer
```bash
wget https://releases.midnight.network/indexer-2.1.4.tar.gz
tar -xzf indexer-2.1.4.tar.gz
cd midnight-indexer
```

### 4. Configure
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

### 5. Run Migrations
```bash
./midnight-indexer migrate --config indexer-config.yaml
```

### 6. Start Indexer
```bash
./midnight-indexer start --config indexer-config.yaml
```

## GraphQL API

Indexer exposes GraphQL API on port 3000:
```
http://localhost:3000/graphql
```

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
