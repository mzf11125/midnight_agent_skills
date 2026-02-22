# Docker Deployment Guide

## Overview

Docker is the recommended deployment method for Midnight Network nodes. This guide covers single-node, multi-node, and production deployments using Docker and Docker Compose.

## Quick Start

### Single Node (Development)

```bash
docker run -d \
  --name midnight-node \
  -p 30333:30333 \
  -p 9933:9933 \
  -p 9944:9944 \
  -v midnight-data:/data \
  ghcr.io/midnight-ntwrk/midnight:latest \
  --chain testnet \
  --rpc-external \
  --ws-external \
  --rpc-cors all
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  midnight-node:
    image: ghcr.io/midnight-ntwrk/midnight:latest
    container_name: midnight-node
    ports:
      - "30333:30333"
      - "9933:9933"
      - "9944:9944"
    volumes:
      - midnight-data:/data
    command:
      - --chain=testnet
      - --rpc-external
      - --ws-external
      - --rpc-cors=all
    restart: unless-stopped

volumes:
  midnight-data:
```

**Start**:
```bash
docker-compose up -d
```

## Image Variants

### Official Images

**Latest stable**:
```bash
ghcr.io/midnight-ntwrk/midnight:latest
```

**Specific version**:
```bash
ghcr.io/midnight-ntwrk/midnight:v2.0.0
```

**Network-specific**:
```bash
ghcr.io/midnight-ntwrk/midnight:testnet
ghcr.io/midnight-ntwrk/midnight:preprod
ghcr.io/midnight-ntwrk/midnight:mainnet
```

### Image Tags

| Tag | Description | Use Case |
|-----|-------------|----------|
| `latest` | Latest stable release | Production |
| `v2.0.0` | Specific version | Version pinning |
| `testnet` | Testnet optimized | Testing |
| `preprod` | Pre-production | Staging |
| `mainnet` | Mainnet optimized | Production |
| `dev` | Development build | Development |

## Production Deployment

### Full Node

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  midnight-node:
    image: ghcr.io/midnight-ntwrk/midnight:v2.0.0
    container_name: midnight-full-node
    hostname: midnight-node
    
    ports:
      - "30333:30333"  # P2P
      - "127.0.0.1:9933:9933"  # RPC (localhost only)
      - "127.0.0.1:9944:9944"  # WebSocket (localhost only)
      - "127.0.0.1:9615:9615"  # Metrics (localhost only)
    
    volumes:
      - midnight-data:/data
      - ./config:/config:ro
    
    environment:
      - RUST_LOG=info,midnight=debug
      - MIDNIGHT_NETWORK=testnet
    
    command:
      - --chain=testnet
      - --base-path=/data
      - --name=MyFullNode
      - --rpc-port=9933
      - --ws-port=9944
      - --rpc-cors=all
      - --rpc-methods=safe
      - --pruning=256
      - --prometheus-external
      - --prometheus-port=9615
    
    restart: unless-stopped
    
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "3"
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9933/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  midnight-data:
    driver: local
```

### Archive Node

```yaml
version: '3.8'

services:
  midnight-archive:
    image: ghcr.io/midnight-ntwrk/midnight:v2.0.0
    container_name: midnight-archive-node
    
    ports:
      - "30333:30333"
      - "127.0.0.1:9933:9933"
      - "127.0.0.1:9944:9944"
    
    volumes:
      - midnight-archive-data:/data
    
    command:
      - --chain=testnet
      - --base-path=/data
      - --name=MyArchiveNode
      - --pruning=archive
      - --rpc-port=9933
      - --ws-port=9944
      - --rpc-cors=all
      - --rpc-max-connections=1000
      - --ws-max-connections=1000
    
    restart: unless-stopped
    
    deploy:
      resources:
        limits:
          cpus: '8'
          memory: 64G
        reservations:
          cpus: '4'
          memory: 32G

volumes:
  midnight-archive-data:
    driver: local
```

### Validator Node

```yaml
version: '3.8'

services:
  midnight-validator:
    image: ghcr.io/midnight-ntwrk/midnight:v2.0.0
    container_name: midnight-validator
    
    ports:
      - "30333:30333"
    
    volumes:
      - midnight-validator-data:/data
      - ./keys:/keys:ro
    
    environment:
      - RUST_LOG=info,midnight=debug
    
    command:
      - --chain=testnet
      - --base-path=/data
      - --validator
      - --name=MyValidator
      - --rpc-methods=unsafe
      - --ws-external=false
      - --rpc-external=false
      - --prometheus-external
    
    restart: unless-stopped
    
    security_opt:
      - no-new-privileges:true
    
    cap_drop:
      - ALL
    
    cap_add:
      - NET_BIND_SERVICE

volumes:
  midnight-validator-data:
    driver: local
```

## Multi-Node Setup

### High Availability Cluster

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  midnight-node-1:
    image: ghcr.io/midnight-ntwrk/midnight:latest
    container_name: midnight-node-1
    ports:
      - "30333:30333"
      - "9933:9933"
      - "9944:9944"
    volumes:
      - midnight-data-1:/data
    command:
      - --chain=testnet
      - --base-path=/data
      - --name=Node1
    restart: unless-stopped
  
  midnight-node-2:
    image: ghcr.io/midnight-ntwrk/midnight:latest
    container_name: midnight-node-2
    ports:
      - "30334:30333"
      - "9934:9933"
      - "9945:9944"
    volumes:
      - midnight-data-2:/data
    command:
      - --chain=testnet
      - --base-path=/data
      - --name=Node2
    restart: unless-stopped
  
  midnight-node-3:
    image: ghcr.io/midnight-ntwrk/midnight:latest
    container_name: midnight-node-3
    ports:
      - "30335:30333"
      - "9935:9933"
      - "9946:9944"
    volumes:
      - midnight-data-3:/data
    command:
      - --chain=testnet
      - --base-path=/data
      - --name=Node3
    restart: unless-stopped
  
  nginx:
    image: nginx:alpine
    container_name: midnight-lb
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - midnight-node-1
      - midnight-node-2
      - midnight-node-3
    restart: unless-stopped

volumes:
  midnight-data-1:
  midnight-data-2:
  midnight-data-3:
```

**nginx.conf**:
```nginx
upstream midnight_rpc {
    least_conn;
    server midnight-node-1:9933 max_fails=3 fail_timeout=30s;
    server midnight-node-2:9933 max_fails=3 fail_timeout=30s;
    server midnight-node-3:9933 max_fails=3 fail_timeout=30s;
}

upstream midnight_ws {
    least_conn;
    server midnight-node-1:9944 max_fails=3 fail_timeout=30s;
    server midnight-node-2:9944 max_fails=3 fail_timeout=30s;
    server midnight-node-3:9944 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name rpc.mydapp.com;
    
    location / {
        proxy_pass http://midnight_rpc;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 443 ssl;
    server_name ws.mydapp.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://midnight_ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Indexer Deployment

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  midnight-archive:
    image: ghcr.io/midnight-ntwrk/midnight:latest
    container_name: midnight-archive
    ports:
      - "30333:30333"
      - "9933:9933"
      - "9944:9944"
    volumes:
      - midnight-archive:/data
    command:
      - --chain=testnet
      - --base-path=/data
      - --pruning=archive
    restart: unless-stopped
  
  postgres:
    image: postgres:15-alpine
    container_name: midnight-postgres
    environment:
      POSTGRES_DB: midnight_indexer
      POSTGRES_USER: indexer
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
  
  indexer:
    image: ghcr.io/midnight-ntwrk/indexer:v3.0.0
    container_name: midnight-indexer
    environment:
      NODE_URL: ws://midnight-archive:9944
      DATABASE_URL: postgresql://indexer:${DB_PASSWORD}@postgres:5432/midnight_indexer
      NETWORK: testnet
    depends_on:
      - midnight-archive
      - postgres
    restart: unless-stopped
  
  graphql:
    image: ghcr.io/midnight-ntwrk/indexer-graphql:v3.0.0
    container_name: midnight-graphql
    ports:
      - "4000:4000"
    environment:
      DATABASE_URL: postgresql://indexer:${DB_PASSWORD}@postgres:5432/midnight_indexer
    depends_on:
      - postgres
      - indexer
    restart: unless-stopped

volumes:
  midnight-archive:
  postgres-data:
```

## Monitoring Stack

**docker-compose.monitoring.yml**:
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped
  
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
    depends_on:
      - prometheus
    restart: unless-stopped
  
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
```

**prometheus.yml**:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'midnight-node'
    static_configs:
      - targets: ['midnight-node:9615']
  
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

## Environment Configuration

### .env File

```bash
# Network
MIDNIGHT_NETWORK=testnet
MIDNIGHT_CHAIN=midnight-testnet-02

# Node
NODE_NAME=MyNode
NODE_VERSION=v2.0.0

# Ports
P2P_PORT=30333
RPC_PORT=9933
WS_PORT=9944
METRICS_PORT=9615

# Database
DB_PASSWORD=secure_password_here

# Monitoring
GRAFANA_PASSWORD=admin_password_here

# Resources
CPU_LIMIT=4
MEMORY_LIMIT=16G
```

### Load from .env

```yaml
version: '3.8'

services:
  midnight-node:
    image: ghcr.io/midnight-ntwrk/midnight:${NODE_VERSION}
    container_name: ${NODE_NAME}
    ports:
      - "${P2P_PORT}:30333"
      - "${RPC_PORT}:9933"
      - "${WS_PORT}:9944"
    environment:
      - MIDNIGHT_NETWORK=${MIDNIGHT_NETWORK}
    deploy:
      resources:
        limits:
          cpus: '${CPU_LIMIT}'
          memory: ${MEMORY_LIMIT}
```

## Management Commands

### Start Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d midnight-node

# View logs
docker-compose logs -f midnight-node

# Check status
docker-compose ps
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop midnight-node
```

### Update Node

```bash
# Pull latest image
docker-compose pull midnight-node

# Restart with new image
docker-compose up -d midnight-node

# View logs
docker-compose logs -f midnight-node
```

### Backup Data

```bash
# Backup volume
docker run --rm \
  -v midnight-data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/midnight-backup-$(date +%Y%m%d).tar.gz /data

# Restore volume
docker run --rm \
  -v midnight-data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar xzf /backup/midnight-backup-20260222.tar.gz -C /
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs midnight-node

# Check container status
docker ps -a

# Inspect container
docker inspect midnight-node

# Remove and recreate
docker-compose down
docker-compose up -d
```

### High Resource Usage

```bash
# Check resource usage
docker stats midnight-node

# Set resource limits
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 16G
```

### Network Issues

```bash
# Check network
docker network ls
docker network inspect midnight_default

# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

### Volume Issues

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect midnight-data

# Remove volume (WARNING: deletes data)
docker volume rm midnight-data
```

## Security Best Practices

### 1. Use Specific Versions

```yaml
# ✅ Pin version
image: ghcr.io/midnight-ntwrk/midnight:v2.0.0

# ❌ Use latest
image: ghcr.io/midnight-ntwrk/midnight:latest
```

### 2. Limit Exposed Ports

```yaml
# ✅ Bind to localhost
ports:
  - "127.0.0.1:9933:9933"

# ❌ Expose to all
ports:
  - "9933:9933"
```

### 3. Use Secrets

```yaml
# ✅ Use Docker secrets
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  postgres:
    secrets:
      - db_password
```

### 4. Run as Non-Root

```yaml
# ✅ Specify user
user: "1000:1000"

# ✅ Drop capabilities
cap_drop:
  - ALL
```

### 5. Enable Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:9933/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Resources

- **Node Architecture**: See node-architecture.md
- **Validator Guide**: See validator-guide.md
- **Monitoring**: See monitoring.md
- **Docker Docs**: https://docs.docker.com
- **Docker Compose**: https://docs.docker.com/compose
