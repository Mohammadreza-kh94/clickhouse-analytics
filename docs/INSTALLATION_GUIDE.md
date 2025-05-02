# ClickHouse Analytics API Installation Guide

This guide provides detailed instructions for setting up and running the ClickHouse Analytics API using Poetry.

## Prerequisites

- Python 3.8 or newer
- Poetry (dependency management)
- Docker and Docker Compose (optional, for containerized setup)

## Installation Options

You have two options for installing and running the application:

1. **Local installation** with Poetry
2. **Containerized installation** with Docker Compose

## Option 1: Local Installation

### Step 1: Install Poetry

If you don't have Poetry installed:

```bash
# For Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# For Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Verify the installation:

```bash
poetry --version
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/clickhouse-analytics.git
cd clickhouse-analytics
```

### Step 3: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your preferred settings
nano .env
```

### Step 4: Install Dependencies

```bash
# Install project dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Step 5: Set Up ClickHouse

You need a running ClickHouse instance. You can:

**A. Use an existing ClickHouse server:**
Update the `.env` file with your ClickHouse connection details.

**B. Start a local ClickHouse with Docker:**
```bash
docker run -d --name clickhouse-server \
  -p 8123:8123 -p 9000:9000 \
  -e CLICKHOUSE_USER=default \
  -e CLICKHOUSE_PASSWORD=clickhouse \
  -e CLICKHOUSE_DB=analytics \
  clickhouse/clickhouse-server
```

### Step 6: Run the Application

```bash
# Inside the poetry shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using poetry run
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000. The API documentation can be accessed at http://localhost:8000/docs.

## Option 2: Containerized Installation with Docker Compose

Docker Compose allows you to run both the ClickHouse database and the FastAPI application in containers.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/clickhouse-analytics.git
cd clickhouse-analytics
```

### Step 2: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file if needed
nano .env
```

### Step 3: Start the Services

```bash
# Build and start the containers
docker-compose up -d

# To view logs
docker-compose logs -f
```

The API will be available at http://localhost:8000, and the API documentation at http://localhost:8000/docs.

### Step 4: Stopping the Services

```bash
docker-compose down
```

To remove all data (including the ClickHouse volume):

```bash
docker-compose down -v
```

## Verifying the Installation

To verify that the API is working correctly:

1. Access the API documentation: http://localhost:8000/docs
2. Try the health check endpoint: http://localhost:8000/
3. Test tracking a page view using the Swagger UI or with curl:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/events/page-view' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_id": "test-event-001",
    "user_id": "test-user-001",
    "session_id": "test-session-001",
    "page_url": "/test-page",
    "event_time": "2025-05-02T14:30:45Z",
    "load_time": 1000
  }'
```

## Troubleshooting

### Connection Issues with ClickHouse

If you encounter connection issues with ClickHouse:

1. Check that ClickHouse is running:
   ```bash
   # For Docker installation
   docker ps | grep clickhouse
   
   # For local installation
   curl http://localhost:8123
   ```

2. Verify connection settings in the `.env` file:
   ```
   CLICKHOUSE_HOST=localhost
   CLICKHOUSE_PORT=8123
   CLICKHOUSE_USER=default
   CLICKHOUSE_PASSWORD=clickhouse
   CLICKHOUSE_DATABASE=analytics
   ```

3. Test a direct connection to ClickHouse:
   ```bash
   curl "http://localhost:8123/?query=SELECT%201"
   ```

### Dependency Issues with Poetry

If you encounter dependency resolution issues with Poetry:

1. Update Poetry:
   ```bash
   poetry self update
   ```

2. Clear Poetry's cache:
   ```bash
   poetry cache clear --all pypi
   ```

3. Try with explicit Python version:
   ```bash
   poetry env use python3.8
   poetry install
   ```

## Next Steps

After successful installation:

1. Explore the API documentation at http://localhost:8000/docs
2. Use the Postman collection for testing
3. Review the CLICKHOUSE_OLAP_GUIDE.md for understanding the OLAP features
4. Check the SCHEMA_DESIGN_GUIDE.md for database schema details