# Midnight Validator Guide

## Validator Registration

Becoming a validator requires registering a Stake Pool Operator identity. The SPO identity links your Cardano stake pool to a Midnight block production identity. Registration submits an onchain transaction that associates your public keys with your stake pool credentials.

### Generating Keys

Generate a set of cryptographic keys for validator operations. The block production key signs blocks during your assigned slots. The VRF key provides the randomness input for leader election. The session keys combine block production and VRF responsibilities. Store all keys in a secure keystore.

### Registration Transaction

Submit the registration transaction through the governance enqueue mechanism. Provide your SPO certificate, session keys, and a bond deposit. The deposit is refundable when you deregister as a validator. Registration takes effect at the start of the following epoch.

## SPO Identity and Pool Management

### Identity Binding

Your SPO identity is cryptographically bound to your Cardano stake pool. Proof of pool ownership is verified during registration. Changes to pool metadata on Cardano propagate to the Midnight chain through periodic sync operations.

### Pool Parameters

Configure pool parameters including the margin, fixed cost, and pledge amount. These parameters affect your delegation attractiveness and rewards calculation. Parameters can be updated between epochs.

### Delegation

Token holders delegate their stake to SPOs to earn staking rewards. Delegation is non custodial meaning the delegator retains control of their tokens. Rewards are distributed proportional to the combined pool stake subject to the pool margin.

## Staking Requirements

### Minimum Stake

Validators must maintain a minimum self stake to participate in block production. The minimum is enforced at epoch boundaries and insufficient stake results in exclusion from the active set.

### Bonding Period

Staked tokens have an unbonding period before they become transferable. This period protects against long range attacks by making stake slashing enforceable. The unbonding period is measured in epochs.

### Slashing Conditions

Validators can be slashed for equivocation, censorship, or prolonged unavailability. Equivocation occurs when a validator signs conflicting blocks at the same height. Slashing penalties are proportional to the severity of the offense and the validator's stake.

## Epoch Performance Tracking

### Block Production Metrics

Track the number of blocks you are assigned versus the number you successfully produce. Target a production rate near 100 percent. Missed blocks reduce your rewards and affect network performance.

### Committee Participation

During your committee term track attendance at consensus rounds. Each missed round degrades the committee's ability to reach agreement. Consistent participation builds a reputation that influences future committee selection weight.

### Dashboard Integration

Export metrics to a Prometheus compatible endpoint. Use Grafana dashboards to visualize epoch performance trends, resource utilization, and node health. Configure alerts for missed blocks, high resource usage, or connectivity issues.

## Committee Participation

### Epoch Assignment

Committee membership rotates each epoch based on stake weighted random selection. The selection algorithm uses a verifiable random function seeded by previous epoch data. All members receive equal voting weight within the committee.

### Consensus Rounds

Each round of block production involves committee members reaching agreement on the next block. Your node must be running and responsive during your assigned slots. Network latency between committee members directly affects block time.

### Backup Planning

Operate a standby node that can take over if your primary node fails. The standby node should share the same keys and be located in a different geographic region. Practice failover procedures regularly.

## Rewards Claiming

### Reward Calculation

Block production rewards are calculated at epoch boundaries based on blocks produced and committee participation. Additional rewards come from transaction fees and protocol inflation. The reward formula accounts for your pool's total stake and performance metrics.

### Claiming Process

Rewards accumulate in a rewards account and must be claimed through an onchain transaction. Claiming is permissionless meaning anyone can trigger the claim for any validator. Unclaimed rewards do not expire but do not compound until claimed.

### Reward Distribution

After claiming, rewards are distributed between the SPO and delegators according to the pool parameters. The margin determines the SPO share and the remainder is split among delegators proportional to their stake.

## Monitoring and Alerting

### Health Metrics

Monitor node uptime, block production rate, peer count, and sync status. Track disk usage growth and memory consumption trends. Set thresholds that trigger alerts before resources become exhausted.

### Alert Configuration

Configure alerts for critical conditions including missed blocks, node downtime, low peer count, and RPC unavailability. Use multiple notification channels such as email, chat platforms, and pager duty integrations.

### Log Aggregation

Ship logs to a centralized log management system. Structure logs in JSON format for easier querying and analysis. Retain logs for a sufficient period to support incident investigation.

## Security Best Practices

### Key Management

Store validator keys in a hardware security module or dedicated key management service. Never store keys on the node's filesystem unencrypted. Rotate session keys periodically while keeping the SPO identity key stable.

### Network Isolation

Place the validator node behind a firewall that blocks direct internet access. Use a sentry architecture where a proxy node faces the public internet and relays traffic to the secured validator. The sentry filters malicious traffic and reduces attack surface.

### Access Control

Restrict SSH access to validator servers to specific IP addresses and enforce key based authentication. Use a jump host or VPN for administrative access. Audit all access attempts and maintain an access log.

### Update Policy

Monitor release announcements and security advisories. Apply security patches within 24 hours of release. Test updates on a staging node before deploying to production. Maintain the ability to roll back to a previous version.

### Incident Response

Prepare an incident response plan covering key compromise, node failure, and network attacks. Document procedures for emergency key rotation and stake withdrawal. Conduct periodic drills to verify response readiness.
