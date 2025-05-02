# Project Structure

This document explains the organization of the ClickHouse Analytics API project.

## Directory Structure

```
clickhouse_analytics/
├── app/                      # Application code
│   ├── __init__.py
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Configuration settings
│   ├── database.py           # ClickHouse connection and utilities
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   ├── schemas.py        # Pydantic models
│   ├── routers/              # API endpoints
│   │   ├── __init__.py
│   │   ├── events.py         # Event tracking endpoints
│   │   ├── analytics.py      # Analytics endpoints
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── events_service.py  # Event tracking logic
│   │   ├── analytics_service.py  # Analytics logic
├── docs/                     # Documentation
│   ├── API_ENDPOINTS_REFERENCE.md
│   ├── CLICKHOUSE_OLAP_GUIDE.md
│   ├── INSTALLATION_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── SCHEMA_DESIGN_GUIDE.md
│   ├── SCALING_GUIDE.md
├── tests/                    # Test files
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_events.py        # Tests for event tracking
│   ├── test_analytics.py     # Tests for analytics
├── .env                      # Environment variables (not in git)
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── client_example.py         # Example client script
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration
├── pyproject.toml            # Poetry project configuration
├── README.md                 # Project README
├── clickhouse_analytics_postman_collection.json  # Postman collection
└── simplified_example.py     # Simplified ClickHouse example
```

## Core Components

### Application Entry Point (app/main.py)

This file initializes the FastAPI application, registers routers, and sets up middleware.

Key responsibilities:
- Initialize FastAPI app with configuration
- Set up CORS middleware
- Register API routers
- Initialize database connection on startup
- Close database connection on shutdown
- Define health check endpoint
- Set up custom Swagger UI documentation

### Configuration (app/config.py)

This file manages application configuration settings, loading from environment variables.

Key responsibilities:
- Load environment variables from .env file
- Define connection settings for ClickHouse
- Define API settings

### Database Connection (app/database.py)

This file handles the ClickHouse database connection and schema initialization.

Key responsibilities:
- Establish connection to ClickHouse
- Initialize database schema (create tables)
- Provide a client accessor function for services
- Handle connection cleanup

### Models (app/models/schemas.py)

This file defines the data models used throughout the application using Pydantic.

Key models:
- `PageView`: Schema for page view events
- `UserAction`: Schema for user action events
- `PageViewResponse`: Response schema for page view tracking
- `UserActionResponse`: Response schema for user action tracking
- `PageViewsAnalytics`: Schema for page views analytics results
- `UserActionsAnalytics`: Schema for user actions analytics results

### Routers

#### Events Router (app/routers/events.py)

This file defines the API endpoints for tracking events.

Endpoints:
- `POST /events/page-view`: Track a page view event
- `POST /events/user-action`: Track a user action event

#### Analytics Router (app/routers/analytics.py)

This file defines the API endpoints for analytics.

Endpoints:
- `GET /analytics/page-views`: Get page views analytics
- `GET /analytics/user-actions`: Get user actions analytics
- `POST /analytics/funnel-analysis`: Perform funnel analysis
- `GET /analytics/retention`: Analyze user retention (placeholder)

### Services

#### Events Service (app/services/events_service.py)

This file contains the business logic for event tracking.

Key functions:
- `insert_page_view`: Insert a page view event into ClickHouse
- `insert_user_action`: Insert a user action event into ClickHouse

#### Analytics Service (app/services/analytics_service.py)

This file contains the business logic for analytics queries.

Key functions:
- `get_page_views_analytics`: Get analytics data for page views
- `get_user_actions_analytics`: Get analytics data for user actions
- `get_funnel_analysis`: Perform funnel analysis for a sequence of pages

## Example Files

### client_example.py

This file provides an example of how to use the API programmatically.

Key features:
- Functions for tracking page views and user actions
- Functions for retrieving analytics data
- Function for simulating user journeys

### simplified_example.py

This file provides a simplified example of using ClickHouse directly without FastAPI.

Key features:
- ClickHouse connection setup
- Table creation
- Data insertion
- Running analytics queries

## Configuration Files

### docker-compose.yml

This file defines the Docker Compose setup for running the application with ClickHouse.

Key components:
- ClickHouse server container
- FastAPI application container
- Volume mounting for persistent data

### pyproject.toml

This file defines the Poetry project configuration, including dependencies.

Key sections:
- Project metadata
- Python dependencies
- Development dependencies
- Build system configuration

## Documentation

The `docs/` directory contains comprehensive documentation for the project:

- `API_ENDPOINTS_REFERENCE.md`: Detailed reference of all API endpoints
- `CLICKHOUSE_OLAP_GUIDE.md`: Guide to ClickHouse's OLAP capabilities
- `INSTALLATION_GUIDE.md`: Instructions for installing and running the application
- `PROJECT_STRUCTURE.md`: This document, explaining the project structure
- `SCHEMA_DESIGN_GUIDE.md`: Guide to the ClickHouse schema design
- `SCALING_GUIDE.md`: Strategies for scaling the application

## Testing

The `tests/` directory contains test files for the application.

Key components:
- `conftest.py`: Test configuration and fixtures
- `test_events.py`: Tests for event tracking functionality
- `test_analytics.py`: Tests for analytics functionality

## Environment Variables

The `.env.example` file documents the environment variables used by the application:

- ClickHouse connection settings
- API settings
- Server settings
- Application settings

Copy this file to `.env` and modify as needed for your environment.