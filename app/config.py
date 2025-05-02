import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# ClickHouse connection settings
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "analytics")

# API settings
API_PREFIX = "/api/v1"