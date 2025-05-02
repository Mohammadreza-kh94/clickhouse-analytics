import clickhouse_connect
from clickhouse_connect.driver.client import Client
from app.config import (
    CLICKHOUSE_HOST,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USER,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_DATABASE,
)

# Global client instance
clickhouse_client: Client | None = None


def get_clickhouse_client() -> Client:
    """
    Get or create a ClickHouse client instance.
    Returns a singleton client to avoid creating multiple connections.
    """
    global clickhouse_client
    if clickhouse_client is None:
        clickhouse_client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE,
        )
    return clickhouse_client


def init_database():
    """
    Initialize the database schema if it doesn't exist.
    Creates the database and necessary tables.
    """
    client = get_clickhouse_client()

    # Create database if it doesn't exist
    client.command(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DATABASE}")

    # Create page_views table
    client.command("""
    CREATE TABLE IF NOT EXISTS page_views (
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
    """)

    # Create user_actions table
    client.command("""
    CREATE TABLE IF NOT EXISTS user_actions (
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
    """)

    print("Database initialization completed")


def close_connection():
    """Close the ClickHouse client connection when the application shuts down."""
    global clickhouse_client
    if clickhouse_client is not None:
        clickhouse_client.close()
        clickhouse_client = None