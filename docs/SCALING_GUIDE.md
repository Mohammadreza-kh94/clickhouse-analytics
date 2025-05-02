# Scaling the ClickHouse Analytics API

This guide provides strategies for scaling the ClickHouse Analytics API to handle larger data volumes and higher traffic.

## When to Scale

Consider scaling your implementation when:

- Query response times exceed acceptable thresholds
- Data volume grows beyond a single server's capacity
- Write throughput becomes a bottleneck
- High availability is required

## Scaling ClickHouse

### 1. Vertical Scaling

The simplest approach is to increase the resources on your ClickHouse server:

```yaml
# Example docker-compose.yml with increased resources
services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse-server
    ports:
      - "8123:8123"
      - "9000:9000"
    deploy:
      resources:
        limits:
          cpus: '8'
          memory: 16G
    volumes:
      - clickhouse-data:/var/lib/clickhouse
    environment:
      - CLICKHOUSE_USER=default
      - CLICKHOUSE_PASSWORD=clickhouse
      - CLICKHOUSE_DB=analytics
```

### 2. Horizontal Scaling with Sharding

For larger deployments, set up a ClickHouse cluster with sharding:

#### Step 1: Configure a ClickHouse Cluster

Create a `config.xml` configuration:

```xml
<clickhouse>
    <remote_servers>
        <analytics_cluster>
            <shard>
                <replica>
                    <host>clickhouse-01</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>clickhouse-02</host>
                    <port>9000</port>
                </replica>
            </shard>
        </analytics_cluster>
    </remote_servers>
</clickhouse>
```

#### Step 2: Create Distributed Tables

On each shard, create local tables:

```sql
CREATE TABLE page_views_local (
    -- Same schema as page_views
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id);
```

Then create a distributed table on each node:

```sql
CREATE TABLE page_views AS page_views_local
ENGINE = Distributed(analytics_cluster, default, page_views_local, rand());
```

#### Step 3: Update Application Configuration

Update the database connection in your application to use any node in the cluster as an entry point.

### 3. Replication for High Availability

Add replicas to each shard for high availability:

```xml
<clickhouse>
    <remote_servers>
        <analytics_cluster>
            <shard>
                <replica>
                    <host>clickhouse-01</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-01-replica</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>clickhouse-02</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-02-replica</host>
                    <port>9000</port>
                </replica>
            </shard>
        </analytics_cluster>
    </remote_servers>
    
    <zookeeper>
        <node>
            <host>zookeeper-01</host>
            <port>2181</port>
        </node>
        <node>
            <host>zookeeper-02</host>
            <port>2181</port>
        </node>
        <node>
            <host>zookeeper-03</host>
            <port>2181</port>
        </node>
    </zookeeper>
</clickhouse>
```

Use ReplicatedMergeTree instead of MergeTree for the local tables:

```sql
CREATE TABLE page_views_local (
    -- Same schema as page_views
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/page_views', '{replica}')
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id);
```

## Scaling the FastAPI Application

### 1. Multiple Application Instances

Run multiple instances behind a load balancer:

```yaml
# Example docker-compose.yml with multiple API instances
services:
  api1:
    build: .
    ports:
      - "8001:8000"
    environment:
      - CLICKHOUSE_HOST=clickhouse
  
  api2:
    build: .
    ports:
      - "8002:8000"
    environment:
      - CLICKHOUSE_HOST=clickhouse
  
  api3:
    build: .
    ports:
      - "8003:8000"
    environment:
      - CLICKHOUSE_HOST=clickhouse
  
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api1
      - api2
      - api3
```

Sample Nginx configuration:

```nginx
http {
    upstream api_servers {
        server api1:8000;
        server api2:8000;
        server api3:8000;
    }
    
    server {
        listen 80;
        
        location / {
            proxy_pass http://api_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### 2. Asynchronous Event Processing

For high-throughput event tracking, implement a message queue:

```python
# Example with Redis Queue
from rq import Queue
from redis import Redis
from app.services import events_service

redis_conn = Redis(host='redis', port=6379)
q = Queue('events', connection=redis_conn)

@router.post("/page-view", response_model=PageViewResponse)
async def track_page_view(page_view: PageView):
    """Track a page view event asynchronously"""
    # Enqueue the job instead of processing immediately
    job = q.enqueue(events_service.insert_page_view, page_view)
    return PageViewResponse(
        event_id=page_view.event_id,
        success=True,
        message="Page view queued for tracking"
    )
```

Update docker-compose.yml to include Redis:

```yaml
services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
  
  worker:
    build: .
    command: rq worker --url redis://redis:6379 events
    depends_on:
      - redis
      - clickhouse
```

## Performance Optimizations

### 1. Materialized Views

Create materialized views for common query patterns:

```sql
CREATE MATERIALIZED VIEW page_views_daily_mv
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(day)
ORDER BY (day, page_url)
AS SELECT
    toDate(event_time) AS day,
    page_url,
    count() AS views,
    uniqExact(user_id) AS unique_visitors,
    avg(load_time) AS avg_load_time
FROM page_views
GROUP BY day, page_url;
```

Update your service to use the materialized view:

```python
def get_page_views_by_day(start_date: datetime, end_date: datetime):
    """Get daily page views from the materialized view"""
    client = get_clickhouse_client()
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    query = f"""
    SELECT
        day,
        sum(views) AS total_views,
        sum(unique_visitors) AS total_unique_visitors
    FROM page_views_daily_mv
    WHERE day BETWEEN '{start_date_str}' AND '{end_date_str}'
    GROUP BY day
    ORDER BY day
    """
    
    return client.query(query).result_rows
```

### 2. Optimized Data Types

Update your schema to use more efficient data types:

```sql
ALTER TABLE page_views
    MODIFY COLUMN user_id UUID,  -- If using UUIDs
    MODIFY COLUMN device_type LowCardinality(String),
    MODIFY COLUMN browser LowCardinality(String),
    MODIFY COLUMN os LowCardinality(String),
    MODIFY COLUMN country LowCardinality(String);
```

### 3. Batch Inserts

Implement batch inserts for better write performance:

```python
def batch_insert_page_views(page_views: List[PageView]):
    """Insert multiple page views in a single batch"""
    client = get_clickhouse_client()
    
    # Prepare data for insertion
    data = []
    for pv in page_views:
        data.append([
            pv.event_id,
            pv.user_id,
            pv.session_id,
            # ... other fields
        ])
    
    # Insert data in a single batch
    client.insert(
        'page_views',
        data,
        column_names=[
            'event_id', 'user_id', 'session_id',
            # ... other columns
        ]
    )
    
    return len(data)
```

## Monitoring and Maintenance

### 1. Set Up Monitoring

Monitor ClickHouse performance:

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

### 2. Implement Data Retention

Set up TTL for automatic data cleanup:

```sql
ALTER TABLE page_views
    MODIFY TTL event_time + INTERVAL 1 YEAR DELETE;

ALTER TABLE user_actions
    MODIFY TTL event_time + INTERVAL 1 YEAR DELETE;
```

### 3. Optimize MergeTree Parts

Periodically optimize MergeTree parts:

```sql
OPTIMIZE TABLE page_views FINAL;
OPTIMIZE TABLE user_actions FINAL;
```

## Cloud Deployment Options

For production environments, consider these cloud options:

1. **ClickHouse Cloud**: Managed ClickHouse service
2. **Self-hosted on cloud VMs**: Deploy on AWS EC2, Google Compute Engine, etc.
3. **Kubernetes deployment**: Use Kubernetes and the ClickHouse Operator

Example Kubernetes configuration for ClickHouse (snippet):

```yaml
apiVersion: "clickhouse.altinity.com/v1"
kind: "ClickHouseInstallation"
metadata:
  name: "analytics-cluster"
spec:
  configuration:
    clusters:
      - name: "analytics"
        layout:
          shardsCount: 2
          replicasCount: 2
```

## Conclusion

Scaling the ClickHouse Analytics API requires a combination of:

1. Database scaling strategies (vertical, horizontal, replication)
2. Application scaling (multiple instances, asynchronous processing)
3. Performance optimizations (materialized views, data types, batch processing)
4. Proper monitoring and maintenance

By implementing these strategies, you can handle growing data volumes and traffic while maintaining good performance.