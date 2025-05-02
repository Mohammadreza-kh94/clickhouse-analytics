# ClickHouse Analytics API

A FastAPI application for tracking and analyzing website events using ClickHouse as an OLAP database.

## Overview

This project demonstrates how to use ClickHouse, a column-oriented database designed for OLAP (Online Analytical Processing), to build a web analytics platform. It includes:

- Event tracking endpoints for page views and user actions
- Analytics endpoints for insights and reporting
- FastAPI for the web API framework
- Poetry for dependency management
- Docker and Docker Compose for easy deployment

## Features

### Event Tracking

- Track page views with detailed metadata
- Track user actions like clicks, form submissions, etc.
- Efficient data storage using ClickHouse's MergeTree engine

### Analytics

- Page view statistics (total views, unique visitors, etc.)
- User action analysis
- Funnel analysis for conversion tracking
- Time-based analysis

### API Documentation

- Interactive Swagger UI documentation
- Postman collection for testing
- Comprehensive markdown documentation

## Quick Start

### Using Docker Compose

The easiest way to get started is with Docker Compose:

```bash
# Clone the repository
git clone https://github.com/yourusername/clickhouse-analytics.git
cd clickhouse-analytics

# Start the application and ClickHouse with Docker Compose
docker-compose up -d

# Access the API at http://localhost:8000
# Access the documentation at http://localhost:8000/docs
```

### Using Poetry (Local Development)

If you prefer to run the application locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/clickhouse-analytics.git
cd clickhouse-analytics

# Install dependencies with Poetry
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your ClickHouse connection details

# Run the application
poetry run uvicorn app.main:app --reload
```

## Documentation

The project includes comprehensive documentation:

- [API Endpoints Reference](docs/API_ENDPOINTS_REFERENCE.md)
- [ClickHouse OLAP Guide](docs/CLICKHOUSE_OLAP_GUIDE.md)
- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Schema Design Guide](docs/SCHEMA_DESIGN_GUIDE.md)
- [Scaling Guide](docs/SCALING_GUIDE.md)

## Example Usage

### Track a Page View

```python
import requests
import uuid
from datetime import datetime

event_id = str(uuid.uuid4())
page_view_data = {
    "event_id": event_id,
    "user_id": "user123",
    "session_id": "session456",
    "page_url": "/products/123",
    "referrer": "https://google.com",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "ip_address": "192.168.1.1",
    "country": "United States",
    "city": "New York",
    "device_type": "desktop",
    "browser": "Chrome",
    "os": "Windows",
    "event_time": datetime.now().isoformat(),
    "load_time": 1200
}

response = requests.post(
    "http://localhost:8000/api/v1/events/page-view",
    json=page_view_data
)

print(response.json())
```

### Get Analytics

```python
import requests
from datetime import datetime, timedelta

# Set date range for analytics
start_date = (datetime.now() - timedelta(days=30)).isoformat()
end_date = datetime.now().isoformat()

# Get page view analytics
response = requests.get(
    f"http://localhost:8000/api/v1/analytics/page-views?start_date={start_date}&end_date={end_date}"
)

print(response.json())
```

See the `client_example.py` file for more detailed examples.

## Project Structure

```
clickhouse_analytics/
├── app/                      # Application code
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Configuration settings
│   ├── database.py           # ClickHouse connection and utilities
│   ├── models/               # Data models
│   ├── routers/              # API endpoints
│   ├── services/             # Business logic
├── docs/                     # Documentation
├── tests/                    # Test files
└── ...                       # Other configuration files
```

For a detailed explanation of the project structure, see [Project Structure](docs/PROJECT_STRUCTURE.md).

## ClickHouse as an OLAP Database

ClickHouse is a column-oriented database management system (DBMS) designed for OLAP workloads. Key features include:

- Columnar storage for efficient analytics queries
- MergeTree engine for fast inserts and reads
- Partitioning for improved query performance
- Powerful aggregation functions
- Support for real-time analytics

For more information about ClickHouse and OLAP, see [ClickHouse OLAP Guide](docs/CLICKHOUSE_OLAP_GUIDE.md).

## Schema Design

The application uses two main tables:

- `page_views`: Stores information about page visits
- `user_actions`: Tracks user interactions like clicks and form submissions

Both tables use the MergeTree engine and are partitioned by month for optimal query performance.

For more details about the schema design, see [Schema Design Guide](docs/SCHEMA_DESIGN_GUIDE.md).

## Scaling

The application can be scaled to handle larger data volumes and higher traffic. Strategies include:

- Vertical scaling (increasing resources)
- Horizontal scaling with ClickHouse sharding
- Replication for high availability
- Asynchronous event processing
- Performance optimizations

For more information, see [Scaling Guide](docs/SCALING_GUIDE.md).

## Testing

The project includes a testing framework using pytest. To run the tests:

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app
```

For more information about testing, see [Testing Guide](docs/TESTING_GUIDE.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.