# ClickHouse Analytics API Documentation Guide

This guide explains how to use the API documentation for the ClickHouse Analytics project.

## Swagger Documentation

FastAPI automatically generates interactive API documentation using Swagger UI.

### Accessing Swagger UI

1. Start your application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

### Using Swagger UI

The Swagger UI provides:

- A list of all available endpoints grouped by tags
- Interactive request builders with schema validation
- Request/response examples
- The ability to try API calls directly from the browser

For each endpoint, you can:

1. Click on the endpoint to expand it
2. View the request parameters and response schema
3. Click the "Try it out" button
4. Fill in the required parameters
5. Click "Execute" to make a live API call
6. See the response

## Postman Collection

For more advanced API testing and usage, we've provided a Postman collection.

### Importing the Collection

1. Open Postman
2. Click "Import" in the top-left corner
3. Upload the `clickhouse_analytics_postman_collection.json` file
4. The collection will appear in your Postman workspace

### Collection Variables

The collection includes these variables:

- `base_url`: The base URL of the API (default: `http://localhost:8000`)
- `start_date`: Start date for analytics queries
- `end_date`: End date for analytics queries

You can edit these variables by:

1. Clicking on the collection name
2. Going to the "Variables" tab
3. Updating the values

### Using the Collection

The collection is organized into folders:

1. **Health Check**: Simple endpoint to check if the API is running
2. **Events**: Endpoints for tracking page views and user actions
3. **Analytics**: Endpoints for retrieving analytics data

Each request includes:

- Pre-configured headers
- Example request bodies with variables
- Description of the endpoint's purpose

### Dynamic Variables

The collection uses Postman's dynamic variables:

- `{{$guid}}`: Generates a unique ID for event tracking
- `{{$isoTimestamp}}`: Inserts the current date and time in ISO format

## API Endpoints Overview

### Event Tracking

- `POST /api/v1/events/page-view`: Track a page view event
- `POST /api/v1/events/user-action`: Track a user action event

### Analytics

- `GET /api/v1/analytics/page-views`: Get page view analytics
- `GET /api/v1/analytics/user-actions`: Get user action analytics
- `POST /api/v1/analytics/funnel-analysis`: Perform funnel analysis

## Example Usage

### Tracking a Page View

Using Postman:
1. Open the "Track Page View" request
2. The request body contains a template with variables
3. Click "Send" to submit the request

Using curl:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/events/page-view' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_id": "12345-uuid-here",
    "user_id": "user123",
    "session_id": "session456",
    "page_url": "/products/123",
    "event_time": "2025-05-02T14:30:45Z",
    "load_time": 1200
  }'
```

### Getting Analytics

Using Postman:
1. Open the "Get Page Views Analytics" request
2. Set the date range using the query parameters
3. Click "Send" to submit the request

Using curl:
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/analytics/page-views?start_date=2025-04-02T00:00:00Z&end_date=2025-05-02T23:59:59Z'
```

## Authentication

The API currently doesn't implement authentication. For production use, you should add authentication mechanisms like OAuth2 or API keys.