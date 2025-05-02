# ClickHouse Schema Design Guide

This guide explains the schema design decisions made in the ClickHouse Analytics API and provides guidance for extending or customizing the schema for your specific needs.

## Current Schema

The application uses two main tables:

### 1. page_views

```sql
CREATE TABLE page_views (
    event_id String,
    user_id String,
    session_id String,
    page_url String,
    referrer String,
    user_agent String,
    ip_address String,
    country String,
    city String,
    device_type String,
    browser String,
    os String,
    event_time DateTime,
    load_time UInt32,
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id)
```

### 2. user_actions

```sql
CREATE TABLE user_actions (
    event_id String,
    user_id String,
    session_id String,
    page_url String,
    action_type String,
    action_data String,
    event_time DateTime,
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id)
```

## Design Decisions Explained

### Table Engine: MergeTree

We use the MergeTree engine, which is ClickHouse's most versatile and performant table engine for analytics workloads. Key benefits:

- Efficient reads and writes
- Support for partitioning
- Primary key indexing
- Background data merging for optimization

### Partitioning Strategy

```sql
PARTITION BY toYYYYMM(event_time)
```

We partition by month using the `toYYYYMM` function on the `event_time` column. This provides:

- Improved query performance for time-based filters
- Efficient storage management
- Automated data lifecycle management

### Sort Key

```sql
ORDER BY (event_time, user_id)
```

The sort key influences:
- Data locality on disk
- Primary index efficiency
- Performance of range queries

We chose (event_time, user_id) as the sort key because:
- Most queries filter by time range
- Many queries analyze user behavior over time
- This combination provides good selectivity

### Column Types

We've chosen specific column types for efficiency:

- **String**: For variable-length text data
- **DateTime**: For timestamp data
- **UInt32**: For unsigned integer data like load_time

### Default Values

```sql
created_at DateTime DEFAULT now()
```

We use DEFAULT constraints to automatically populate values like `created_at` to track when records are inserted.

## Optimizing for Common Queries

Our schema is optimized for the following query patterns:

1. **Time-range queries**: Filtering by date range is efficient due to partitioning and sort key
2. **User-based analysis**: Queries filtering by user_id are efficient due to the sort key
3. **Aggregation queries**: Columnar storage makes aggregation operations fast

## Schema Extension Recommendations

When extending the schema, consider these guidelines:

### Adding New Columns

You can add new columns to existing tables using ALTER TABLE:

```sql
ALTER TABLE page_views ADD COLUMN new_column_name DataType;
```

ClickHouse allows adding columns with minimal overhead.

### Adding New Tables

When adding new tables, follow these patterns:

```sql
CREATE TABLE new_table (
    /* Primary identifiers */
    event_id String,
    
    /* Entity relationships */
    user_id String,
    
    /* Event data */
    /* ... your specific columns ... */
    
    /* Time dimensions */
    event_time DateTime,
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id)
```

### Optimizing Column Types

For better performance, consider these specialized types:

- Replace high-cardinality String columns with **UUID** if they're UUIDs
- Replace low-cardinality String columns with **LowCardinality(String)** for better compression
- Use **Enum** for fields with a fixed set of possible values
- Use **DateTime64** for timestamps requiring sub-second precision
- Use **IPv4** or **IPv6** for IP addresses instead of String

Example optimization:

```sql
-- Before
action_type String,

-- After (if action_type has few possible values)
action_type LowCardinality(String),
```

### Materialized Views

For common query patterns, consider creating materialized views to pre-aggregate data:

```sql
CREATE MATERIALIZED VIEW page_views_daily_mv
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(day)
ORDER BY (day, page_url)
AS SELECT
    toDate(event_time) AS day,
    page_url,
    count() AS views,
    count(DISTINCT user_id) AS unique_visitors,
    avg(load_time) AS avg_load_time
FROM page_views
GROUP BY day, page_url;
```

### Sharding and Distributed Tables

For larger deployments, consider sharding your data:

```sql
-- On each shard
CREATE TABLE page_views_local (/* schema */)
ENGINE = MergeTree()
-- ... rest of the definition

-- On the coordination server
CREATE TABLE page_views AS page_views_local
ENGINE = Distributed(cluster_name, default, page_views_local, rand());
```

## Data Lifecycle Management

For production environments, implement data lifecycle policies:

```sql
ALTER TABLE page_views
    MODIFY TTL event_time + INTERVAL 1 YEAR DELETE;
```

This automatically removes data older than one year.

## Monitoring Schema Performance

Regularly check these system tables to monitor schema performance:

```sql
-- Check table sizes
SELECT
    table,
    formatReadableSize(sum(bytes)) AS size,
    count() AS parts
FROM system.parts
WHERE active AND database = 'analytics'
GROUP BY table
ORDER BY sum(bytes) DESC;

-- Check query performance
SELECT
    type,
    formatReadableSize(memory_usage) AS memory,
    query_duration_ms / 1000 AS duration_seconds,
    query
FROM system.query_log
WHERE type = 'QueryFinish' AND query NOT LIKE '%system%'
ORDER BY query_duration_ms DESC
LIMIT 10;
```

## Conclusion

The ClickHouse schema design for this API follows best practices for OLAP workloads. The MergeTree engine, monthly partitioning, and appropriate sort keys provide a solid foundation for analytical queries. When extending the schema, maintain these patterns and consider specialized column types and materialized views for optimal performance.