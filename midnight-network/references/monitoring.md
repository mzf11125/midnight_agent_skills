# Monitoring and Troubleshooting

## Health Checks

### Node Health
```bash
curl http://localhost:9933/health
```

Expected response:
```json
{
  "status": "healthy",
  "peers": 25,
  "syncing": false,
  "blockHeight": 123456
}
```

### Indexer Health
```bash
curl http://localhost:3000/health
```

### Validator Status
```bash
./midnight-node validator-status
```

## Key Metrics

### Node Metrics
- **Peer Count**: Should be > 10
- **Block Height**: Should match network
- **Sync Status**: Should be false (synced)
- **Memory Usage**: Monitor for leaks
- **Disk Usage**: Ensure sufficient space

### Validator Metrics
- **Blocks Produced**: Track production rate
- **Missed Blocks**: Should be minimal
- **Stake**: Verify stake is active
- **Rewards**: Monitor reward accumulation

### Indexer Metrics
- **Sync Lag**: Should be < 10 blocks
- **Query Performance**: Monitor response times
- **Database Size**: Track growth
- **Error Rate**: Should be near zero

## Common Issues

### Node Not Syncing
**Symptoms**: Block height not increasing
**Solutions**:
- Check network connectivity
- Verify bootnode connections
- Check disk space
- Restart node

### Validator Not Producing Blocks
**Symptoms**: No blocks produced
**Solutions**:
- Verify stake is active
- Check validator keys
- Ensure node is synced
- Check for slashing

### Indexer Lag
**Symptoms**: Indexer behind chain
**Solutions**:
- Increase batch size
- Optimize database
- Check node RPC performance
- Add more resources

### High Memory Usage
**Symptoms**: OOM errors
**Solutions**:
- Increase system RAM
- Tune node parameters
- Check for memory leaks
- Restart services

## Alerting

### Critical Alerts
- Node down
- Validator missing blocks
- Indexer stopped
- Disk space < 10%

### Warning Alerts
- High peer churn
- Slow sync speed
- High memory usage
- Database performance degradation

## Logging

### Node Logs
```bash
tail -f /var/log/midnight-node/node.log
```

### Indexer Logs
```bash
tail -f /var/log/midnight-indexer/indexer.log
```

### Log Levels
- ERROR: Critical issues
- WARN: Potential problems
- INFO: Normal operations
- DEBUG: Detailed information

## Best Practices

1. **Monitor Continuously**: Use monitoring tools (Prometheus, Grafana)
2. **Set Up Alerts**: Get notified of issues immediately
3. **Regular Backups**: Backup keys and configurations
4. **Keep Updated**: Apply security patches promptly
5. **Test Failover**: Ensure redundancy works
6. **Document Procedures**: Maintain runbooks
