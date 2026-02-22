# Monitoring and Troubleshooting

## Overview

Comprehensive monitoring and troubleshooting guide for Midnight Network infrastructure including nodes, validators, and indexers.

## Health Checks

### Node Health Check

```bash
# HTTP health endpoint
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_health"}'
```

**Expected response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "peers": 50,
    "isSyncing": false,
    "shouldHavePeers": true
  }
}
```

**Health indicators**:
- `peers > 10`: Good connectivity
- `isSyncing: false`: Node is synced
- `shouldHavePeers: true`: Network configured correctly

### Indexer Health Check

```bash
# Indexer health endpoint
curl http://localhost:8088/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "syncedBlock": 123456,
  "chainBlock": 123460,
  "lag": 4,
  "database": "connected"
}
```

**Health indicators**:
- `lag < 10`: Indexer keeping up
- `database: "connected"`: Database operational
- `status: "healthy"`: All systems operational

### Validator Status

```bash
# Check validator status
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"author_rotateKeys"}'

# Check if validator is active
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"session_validators"}'
```

## Prometheus Metrics

### Enable Metrics

**Node configuration**:
```bash
midnight-node \
  --prometheus-external \
  --prometheus-port 9615
```

**Metrics endpoint**: `http://localhost:9615/metrics`

### Key Metrics

#### Node Metrics

```prometheus
# Block height
substrate_block_height{status="best"}

# Peer count
substrate_sub_libp2p_peers_count

# Sync status
substrate_sub_libp2p_is_major_syncing

# Database size
substrate_database_cache_bytes

# Memory usage
process_resident_memory_bytes

# CPU usage
process_cpu_seconds_total
```

#### Validator Metrics

```prometheus
# Blocks produced
substrate_proposer_block_constructed_count

# Block production time
substrate_proposer_block_constructed

# Finality lag
substrate_finality_grandpa_round

# Validator active
substrate_node_roles{role="authority"}
```

#### Indexer Metrics

```prometheus
# Sync lag
indexer_sync_lag_blocks

# Query latency
indexer_query_duration_seconds

# Database connections
indexer_db_connections_active

# Error rate
indexer_errors_total
```

## Grafana Dashboards

### Setup Grafana

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - prometheus

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
  
  - job_name: 'midnight-indexer'
    static_configs:
      - targets: ['midnight-indexer:9616']
```

### Dashboard Panels

**Node Dashboard**:
- Block height over time
- Peer count
- Sync status
- Memory/CPU usage
- Disk I/O
- Network traffic

**Validator Dashboard**:
- Blocks produced
- Missed blocks
- Finality lag
- Stake amount
- Rewards earned
- Slash events

**Indexer Dashboard**:
- Sync lag
- Query latency (p50, p95, p99)
- Database size
- Connection pool
- Error rate
- Throughput (queries/sec)

## Logging

### Log Configuration

**Node logging**:
```bash
# Set log level
RUST_LOG=info,midnight=debug midnight-node

# Log to file
midnight-node 2>&1 | tee /var/log/midnight/node.log

# Rotate logs
logrotate /etc/logrotate.d/midnight-node
```

**Logrotate config** (`/etc/logrotate.d/midnight-node`):
```
/var/log/midnight/node.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 midnight midnight
}
```

### Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| ERROR | Critical failures | Production alerts |
| WARN | Potential issues | Investigation needed |
| INFO | Normal operations | General monitoring |
| DEBUG | Detailed info | Development/troubleshooting |
| TRACE | Very detailed | Deep debugging |

### Useful Log Queries

**Find errors**:
```bash
grep "ERROR" /var/log/midnight/node.log | tail -n 50
```

**Monitor in real-time**:
```bash
tail -f /var/log/midnight/node.log | grep -E "ERROR|WARN"
```

**Count errors by type**:
```bash
grep "ERROR" /var/log/midnight/node.log | awk '{print $5}' | sort | uniq -c
```

## Alerting

### Alert Rules

**Prometheus alerts** (`alerts.yml`):
```yaml
groups:
  - name: midnight_node
    interval: 30s
    rules:
      # Node down
      - alert: NodeDown
        expr: up{job="midnight-node"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Midnight node is down"
      
      # Low peer count
      - alert: LowPeerCount
        expr: substrate_sub_libp2p_peers_count < 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low peer count: {{ $value }}"
      
      # Node not syncing
      - alert: NodeNotSyncing
        expr: increase(substrate_block_height[5m]) == 0
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Node not producing blocks"
      
      # High memory usage
      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes > 30e9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Memory usage > 30GB"
      
      # Disk space low
      - alert: DiskSpaceLow
        expr: node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes < 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space < 10%"

  - name: midnight_validator
    interval: 30s
    rules:
      # Validator not producing blocks
      - alert: ValidatorNotProducing
        expr: increase(substrate_proposer_block_constructed_count[10m]) == 0
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Validator not producing blocks"
      
      # High finality lag
      - alert: HighFinalityLag
        expr: substrate_finality_grandpa_round - substrate_block_height > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Finality lag > 10 blocks"

  - name: midnight_indexer
    interval: 30s
    rules:
      # Indexer lag
      - alert: IndexerLag
        expr: indexer_sync_lag_blocks > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Indexer lag > 100 blocks"
      
      # High query latency
      - alert: HighQueryLatency
        expr: histogram_quantile(0.95, indexer_query_duration_seconds) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Query p95 latency > 1s"
```

### Notification Channels

**Slack integration**:
```yaml
receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
        channel: '#midnight-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.summary }}'
```

**Email integration**:
```yaml
receivers:
  - name: 'email'
    email_configs:
      - to: 'ops@example.com'
        from: 'alerts@midnight.network'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'alerts@midnight.network'
        auth_password: 'password'
```

**PagerDuty integration**:
```yaml
receivers:
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_SERVICE_KEY'
```

## Common Issues

### Node Not Syncing

**Symptoms**:
- Block height not increasing
- `isSyncing: true` persists
- Peer count low

**Diagnosis**:
```bash
# Check sync status
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_syncState"}'

# Check peers
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_peers"}'

# Check logs
grep "sync" /var/log/midnight/node.log | tail -n 50
```

**Solutions**:
1. Check network connectivity
2. Add bootnodes: `--bootnodes /dns/bootnode.midnight.network/tcp/30333/p2p/...`
3. Check firewall: Allow port 30333
4. Verify disk space: `df -h`
5. Restart node: `systemctl restart midnight-node`

### Validator Not Producing Blocks

**Symptoms**:
- No blocks produced in last hour
- Validator not in active set
- Missing block rewards

**Diagnosis**:
```bash
# Check if validator is active
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"session_validators"}'

# Check validator keys
ls -la /keys/validator.key

# Check stake
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"staking_ledger", "params":["VALIDATOR_ADDRESS"]}'
```

**Solutions**:
1. Verify stake is active and sufficient
2. Check validator keys are loaded
3. Ensure node is fully synced
4. Check for slashing events
5. Verify session keys are set correctly

### Indexer Lag

**Symptoms**:
- Indexer blocks behind chain
- Slow query responses
- Stale data in DApp

**Diagnosis**:
```bash
# Check indexer status
curl http://localhost:8088/status

# Check database performance
psql -U indexer -d midnight_indexer -c "SELECT pg_size_pretty(pg_database_size('midnight_indexer'));"

# Check logs
grep "lag" /var/log/midnight/indexer.log | tail -n 50
```

**Solutions**:
1. Increase batch size in config
2. Optimize database indexes
3. Add more CPU/RAM
4. Check node RPC performance
5. Consider archive node for indexer

### High Memory Usage

**Symptoms**:
- OOM killer terminating processes
- Swap usage high
- System sluggish

**Diagnosis**:
```bash
# Check memory usage
free -h

# Check process memory
ps aux --sort=-%mem | head -n 10

# Check for memory leaks
valgrind --leak-check=full midnight-node
```

**Solutions**:
1. Increase system RAM
2. Enable pruning: `--pruning 256`
3. Reduce cache size: `--db-cache 512`
4. Check for memory leaks in logs
5. Restart node periodically

### Database Issues

**Symptoms**:
- Slow queries
- Connection timeouts
- Database corruption

**Diagnosis**:
```bash
# Check database size
du -sh /data/midnight/chains/*/db

# Check database integrity
midnight-node check-db --chain testnet

# Check PostgreSQL (indexer)
psql -U indexer -d midnight_indexer -c "SELECT * FROM pg_stat_activity;"
```

**Solutions**:
1. Vacuum database: `VACUUM ANALYZE;`
2. Rebuild indexes: `REINDEX DATABASE midnight_indexer;`
3. Increase connection pool
4. Optimize queries
5. Consider database migration

### Network Connectivity Issues

**Symptoms**:
- Cannot connect to peers
- RPC timeouts
- Websocket disconnects

**Diagnosis**:
```bash
# Test connectivity
nc -zv rpc.testnet.midnight.network 443

# Check DNS
nslookup rpc.testnet.midnight.network

# Check firewall
sudo iptables -L -n

# Test websocket
wscat -c wss://rpc.testnet.midnight.network
```

**Solutions**:
1. Check firewall rules
2. Verify DNS resolution
3. Test with different endpoint
4. Check proxy settings
5. Verify SSL certificates

## Performance Tuning

### Node Optimization

```bash
# Increase file descriptors
ulimit -n 65536

# Optimize database cache
--db-cache 4096

# Tune pruning
--pruning 256

# Optimize networking
--max-parallel-downloads 8
--out-peers 25
--in-peers 25
```

### Indexer Optimization

**PostgreSQL tuning** (`postgresql.conf`):
```ini
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 4
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
```

## Best Practices

### 1. Monitor Continuously

```bash
# Use monitoring stack
docker-compose -f monitoring.yml up -d

# Set up dashboards
# Configure alerts
# Review metrics daily
```

### 2. Set Up Alerts

```bash
# Critical alerts
- Node down
- Validator missing blocks
- Disk space < 10%

# Warning alerts
- High memory usage
- Slow sync
- Indexer lag
```

### 3. Regular Backups

```bash
# Backup validator keys
cp /keys/validator.key /backup/validator.key.$(date +%Y%m%d)

# Backup database
pg_dump midnight_indexer > backup.sql

# Backup configuration
tar czf config-backup.tar.gz /etc/midnight/
```

### 4. Keep Updated

```bash
# Check for updates
midnight-node --version

# Update node
docker pull ghcr.io/midnight-ntwrk/midnight:latest
docker-compose up -d

# Verify update
midnight-node --version
```

### 5. Test Failover

```bash
# Test backup node
# Verify monitoring alerts
# Practice recovery procedures
# Document runbooks
```

### 6. Document Procedures

Create runbooks for:
- Node restart procedure
- Validator key rotation
- Database recovery
- Network migration
- Incident response

## Resources

- **Node Architecture**: See node-architecture.md
- **Docker Deployment**: See docker-deployment.md
- **Validator Guide**: See validator-guide.md
- **Prometheus Docs**: https://prometheus.io/docs
- **Grafana Docs**: https://grafana.com/docs
