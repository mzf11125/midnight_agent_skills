# Midnight Indexer Operations Guide

## Indexer Setup and Installation

### Prerequisites

The indexer requires Node.js version 18 or later and PostgreSQL version 15 or later. Install the PostgreSQL client libraries and development headers before building the indexer. Ensure the database server is running and accessible from the indexer host.

### Installation Steps

Clone the indexer repository from the official source. Install dependencies using the package manager. Build the project with the provided build script. Run database migrations to create the required schema. Start the indexer process with the appropriate configuration file.

### Database Initialization

Create a dedicated PostgreSQL database for the indexer. Run the migration scripts to create tables, indexes, and functions. Configure connection pooling with a maximum of 20 connections for production workloads. Set the statement timeout to prevent long running queries from blocking connection slots.

## Configuration Options

### Database Configuration

The database connection string specifies the host, port, database name, user, and password. Use environment variables rather than hardcoded values in configuration files. Enable SSL for connections to remote database servers.

### Network Configuration

Specify the Midnight node RPC endpoint that the indexer connects to for blockchain data. Configure reconnection parameters including maximum retries and backoff strategy. Set the WebSocket endpoint for subscription based data feeds.

### Indexing Configuration

Choose which data domains to index. Options include blocks, transactions, contract state, SPO data, DUST ledger events, and zswap events. Disable indexing for domains you do not need to reduce database size and processing load.

### API Configuration

Configure the GraphQL endpoint port, CORS settings, and rate limits. Set the maximum query depth to prevent complex nested queries from consuming excessive resources. Configure request timeouts appropriate for your expected query patterns.

## Scaling Considerations

### Vertical Scaling

Increase CPU cores and RAM to handle more concurrent queries and faster block processing. NVMe storage significantly improves index building performance. PostgreSQL benefits from large shared buffers and effective cache sizes tuned to available RAM.

### Horizontal Scaling

Deploy read replicas of the PostgreSQL database to distribute query load. Configure the indexer to direct read queries to replicas and write operations to the primary. Use connection pooling at the application layer to manage replica connections.

### Database Partitioning

Partition large tables by time range or block height. This improves query performance and simplifies data archival. Consider partitioning the transactions and contract actions tables which grow the fastest.

### Caching Strategy

Implement an in memory cache for frequently accessed data such as the current epoch, recent blocks, and D parameter values. Use Redis or Memcached as a shared cache when running multiple indexer instances. Set appropriate TTL values based on data update frequency.

## Docker Deployment

### Image Building

Build the indexer Docker image from the provided Dockerfile. Tag images with the git commit hash for traceability. Push images to a private container registry for deployment to production environments.

### Compose Configuration

Create a `docker-compose.yml` that includes the indexer service, PostgreSQL service, and optionally a Redis cache service. Define health checks for each service. Use named volumes for PostgreSQL data and a bind mount or volume for indexer configuration files.

### Environment Management

Pass configuration through environment variables rather than baking them into images. Use Docker secrets or a secrets manager for sensitive values like database credentials and API keys. Provide different `.env` files for development, staging, and production environments.

## Data Model Overview

### Core Entities

The indexer organizes data around blocks, transactions, contract actions, and ledger events. Each entity has a unique identifier and references related entities through foreign keys. Timestamps are stored in UTC without timezone offsets.

### Block Table

The blocks table stores headers including hash, parent hash, height, timestamp, producer identifier, and state root. Additional metadata columns track transaction count, gas used, and the epoch number.

### Transaction Table

The transactions table stores each transaction with its type, status, sender, fee, and payload data. The payload column uses JSONB for flexible schema while allowing indexed queries on common fields.

### Contract Action Table

The contract actions table maps each contract interaction to its parent transaction and block. Input and output references are stored as file paths or content hashes pointing to the external data store.

### Ledger Event Tables

Separate tables store DUST events, token transfer events, and zswap protocol events. Each event type has a schema specific to its data shape with common columns for block height, transaction reference, and timestamp.

## Query Optimization

### Index Strategy

Create composite indexes on the most common filter combinations. Index the block height and timestamp columns for time range queries. Create partial indexes for queries that filter by status or type to reduce index size.

### Query Analysis

Use PostgreSQL EXPLAIN ANALYZE to profile query performance. Look for sequential scans on large tables and add targeted indexes. Monitor slow query logs and set appropriate thresholds for the log_min_duration_statement parameter.

### Connection Pooling

Configure a connection pool with PgBouncer or the built in pool in the indexer application. Set the pool size based on available database connections and expected concurrent query load. Use transaction level pooling for stateless API queries.

## Subscription Lifecycle Management

### Connection Establishment

Clients establish WebSocket connections to the GraphQL endpoint. The connection requires a valid session token obtained through the connect mutation. The server limits concurrent WebSocket connections per client.

### Subscription Registration

After connecting clients send a subscription operation request. The server validates the subscription query and registers the client for event delivery. Subscriptions support filter arguments to receive only relevant events.

### Keepalive and Heartbeat

The server sends periodic keepalive messages to detect client disconnections. Clients that do not respond within the timeout window have their subscriptions terminated. Configure the keepalive interval balancing network overhead with detection speed.

### Reconnection Protocol

When a client disconnects it should attempt to reconnect with exponential backoff. After reconnecting the client must resubscribe to all desired event streams. Use the last received event cursor to avoid missing events during the disconnection window.

## Error Handling and Reconnection

### Transient Errors

Network timeouts and temporary database unavailability trigger automatic retries with backoff. The maximum retry count and backoff multiplier are configurable. Log transient errors at warning level and persistent errors at error level.

### Data Consistency

When the indexer detects a gap in processed blocks it enters a catchup mode. During catchup the indexer processes blocks sequentially until caught up with the current chain tip. Subscriptions resume normal operation once the gap is closed.

### Database Connection Failures

The indexer monitors database connectivity and attempts reconnection when the connection drops. Use connection validation queries to detect stale connections. Implement circuit breaking to prevent cascading failures when the database is unavailable.

## Troubleshooting Guide

### Stalled Indexing

If the indexer stops processing new blocks check the node RPC connectivity. Verify the node is synced and producing blocks. Check indexer logs for database errors that may block writes. Restart the indexer after resolving the underlying issue.

### Slow Queries

Slow GraphQL queries typically indicate missing indexes or poorly structured filters. Review query patterns in production and add indexes for the most common filter fields. Consider adding precomputed aggregate tables for expensive summary queries.

### Memory Issues

High memory usage often results from large result sets being materialized in memory. Enforce pagination limits and maximum query complexity. Monitor the number of active subscriptions which each consume a connection and associated memory.

### Disk Growth

Monitor database disk usage and set up alerts at 75 and 90 percent capacity. Implement a data archival strategy for tables that accumulate historical data. Consider time based partitioning to enable efficient data removal by dropping old partitions.

## Version Compatibility

### Indexer and Node Compatibility

Each indexer version targets a specific node version range. Check the compatibility matrix in the release notes before upgrading either component. Running mismatched versions may cause incorrect data or indexing failures.

### Database Migration Compatibility

Database migrations are forward compatible within a major version. Always back up the database before running migrations. Test migrations on a staging database that mirrors production data before applying to production.

### API Version Policy

The GraphQL API follows a versioning policy where breaking changes increment the major version. Deprecated fields remain available for at least one major version cycle with deprecation notices in the schema. Monitor deprecation warnings and update queries before upgrading to avoid breaking changes.
