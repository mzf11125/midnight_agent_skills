# Midnight Proof Server Operations Guide

## Docker Deployment

### StaticProofServerContainer

The StaticProofServerContainer provides a proof server with a fixed set of preloaded circuits. Circuits and their keys are baked into the container image at build time. This container type is suitable for deployments where the set of supported contracts is known in advance and changes infrequently.

Build the container by specifying the circuits to include in a manifest file. The build process compiles the circuits, generates keys, and packages them into the image. Use multi stage builds to keep the final image size manageable.

Start the container with the `docker run` command providing a port mapping for the proof server API. Mount a volume for logs and temporary proving workspace data. Configure environment variables for resource limits and network specific parameters.

### DynamicProofServerContainer

The DynamicProofServerContainer allows circuits to be loaded at runtime without rebuilding the image. Circuits and keys are stored in a mounted volume or fetched from a key repository at startup. This container type supports deployments where contracts are frequently added or updated.

Configure the container with a circuit directory path and optional key repository URL. The server polls the repository for new circuit versions and automatically loads them. Set the polling interval to balance freshness with repository load.

## Container Configuration

### ContainersConfiguration

The ContainersConfiguration object defines all settings for a proof server deployment. It includes resource limits, timeout values, concurrency settings, circuit definitions, and network specific overrides. This configuration is passed to the container as environment variables or as a mounted configuration file.

### getContainersConfiguration

The `getContainersConfiguration` function reads the current configuration from the running container. It merges default values, environment variable overrides, and configuration file settings to produce the effective configuration. Use this function to inspect the current state before making changes.

### setContainersConfiguration

The `setContainersConfiguration` function applies configuration updates to a running container. It accepts a partial configuration object and validates each field against allowed ranges. Invalid values are rejected with descriptive error messages. Changes that require a worker restart take effect for new jobs while active jobs complete with their existing settings.

## Configuration Tuning

### Timeout Configuration

Each proving job has a maximum execution time. Set the `proofTimeout` value high enough for the most complex circuit but low enough to release resources for stuck jobs. Separate timeout values can be configured for different circuit families. Monitor timeout rates and adjust values based on observed circuit proving times.

Set the `queueTimeout` for how long a job can wait in the queue before being rejected. This prevents queue buildup during traffic spikes at the cost of rejecting late arriving jobs. Clients should implement retry logic with backoff for queue timeout rejections.

### Concurrency Settings

The `maxWorkers` setting controls how many proof generation tasks run simultaneously. Each worker consumes CPU and memory resources. Set this value based on the available CPU cores and memory per worker. Oversubscribing CPU leads to context switching overhead that reduces total throughput.

The `maxQueueDepth` setting limits the number of jobs waiting for a worker. When the queue reaches this limit new jobs are rejected with a capacity exceeded error. Set this high enough to absorb normal traffic bursts but low enough to provide backpressure before the system exhausts resources.

### Resource Allocation

Allocate CPU resources through Docker CPU quotas and shares. Proof generation is CPU intensive and benefits from dedicated cores. Use CPU pinning for cache sensitive workloads on servers with non uniform memory access architecture.

Allocate memory based on the largest circuit that will be proven concurrently. Each worker loads the proving key for its assigned circuit into memory. Sum the memory requirements for the maximum concurrent workers plus overhead for the operating system and other processes. Configure swap as a safety margin but avoid relying on it for performance.

## Performance Optimization

### Key Caching

Load frequently used proving keys into a memory cache that persists across jobs. This avoids disk I/O for each new proving request. Configure the cache size based on available memory and the total size of all loaded keys. Use a least recently used eviction policy when the cache reaches capacity.

### Circuit Preloading

Preload circuits that are expected to be requested based on historical patterns. The proof server can warm its cache during startup by generating sample proofs for popular circuits. This eliminates cold start latency for common proving requests.

### Worker Affinity

Pin worker processes to specific CPU cores to improve cache locality. This reduces cache misses when a worker processes multiple jobs for the same circuit. Configure worker affinity through the container orchestration layer.

### Batch Processing

When clients submit multiple proof requests group them into batches. Batch processing amortizes the overhead of key loading and context switching. Configure the batch window to balance throughput with individual job latency.

## Health Monitoring

### Metrics Collection

The proof server exposes Prometheus metrics at a dedicated endpoint. Key metrics include proof generation latency histograms, queue depth gauge, error rate counter, worker utilization gauge, and key cache hit rate. Configure a Prometheus scrape job for the proof server endpoint.

### Health Endpoint

The health endpoint returns a status code and JSON payload indicating server health. A healthy response requires all workers to be responsive and key material to be loaded. Load balancers use this endpoint to route traffic away from unhealthy instances.

### Logging Configuration

Configure structured JSON logging with timestamps, log levels, and correlation identifiers. Include the proof job identifier in all log entries related to a specific request. Set the log level to `info` for production with the ability to dynamically change to `debug` for troubleshooting.

### Alert Rules

Configure alerts for conditions that require operator attention. Alert when the queue depth exceeds a threshold for more than two minutes. Alert when the error rate exceeds one percent over a five minute window. Alert when worker count drops below the configured minimum indicating worker crashes.

## Error Troubleshooting

### Proof Generation Failures

Proof generation failures typically indicate malformed inputs, circuit incompatibility, or resource exhaustion. Check the error message for specific failure reasons. Verify that the input witness data matches the circuit's expected input format. Confirm the circuit version matches the version expected by the contract.

### Key Loading Failures

Key loading failures occur when the proof server cannot find or parse the required key material. Verify that the key files exist at the configured path. Check file permissions to ensure the proof server process has read access. Validate that key file checksums match expected values to detect corruption.

### Connection Timeouts

Client connection timeouts often result from network configuration issues or overloaded servers. Check that the proof server port is accessible from the client network. Review server resource usage to identify CPU or memory saturation. Increase timeout values if proofs take longer than the configured client timeout.

### Memory Errors

Out of memory errors indicate that the configured memory limits are insufficient for the current workload. Reduce the maximum concurrent workers or increase the memory allocation. Check for memory leaks by monitoring memory usage over time. Key caching may consume more memory than expected if circuit sizes are underestimated.

## Network Specific Configurations

### Local Development Network

For local development configure the proof server with relaxed security settings and lower resource limits. Disable authentication since the server runs on localhost only. Use smaller key sizes and shorter timeouts to speed up the development feedback loop.

### Preview Network

The preview network mirrors mainnet but with test tokens. Configure the proof server with the preview network's circuit versions and key material. Enable authentication if the server is publicly accessible. Use resource limits similar to production to validate performance characteristics before mainnet deployment.

### Preprod Network

The preprod network provides a staging environment before mainnet. Configure the proof server with the exact circuit versions planned for mainnet launch. Run load tests against preprod proof servers to validate capacity planning. Monitor error rates closely as preprod catches integration issues before they affect production.

### Mainnet

Mainnet deployment requires the highest security and reliability standards. Enable strict authentication on all endpoints. Configure redundant proof server instances across multiple availability zones. Implement a blue or green deployment strategy for configuration changes. Monitor all metrics continuously and maintain an on call rotation for incident response.

### Cross Network Key Management

Each network uses separate key material. Maintain distinct key directories for each network to prevent cross network key contamination. Use network tags in key metadata to validate that the correct keys are loaded. Automate key deployment to reduce the risk of manual errors when promoting circuits between networks.
