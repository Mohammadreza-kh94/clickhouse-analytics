# API Endpoints Reference

This document provides a comprehensive reference of all endpoints available in the ClickHouse Analytics API.

## Base URL

All endpoints are prefixed with `/api/v1`.

## Authentication

The API currently doesn't implement authentication. For production use, you should add authentication.

## Health Check

### GET /

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "ClickHouse Analytics API is running"
}
```

## Event Tracking

### POST /api/v1/events/page-view

Track a page view event.

**Request Body:**
```json
{
  "event_id": "string",
  "user_id": "string",
  "session_id": "string",
  "page_url": "string",
  "referrer": "string",
  "user_agent": "string",
  "ip_address": "string",
  "country": "string",
  "city": "string",
  "device_type": "string",
  "browser": "string",
  "os": "string",
  "event_time": "2025-05-02T14:30:45Z",
  "load_time": 1200
}
```

**Response:**
```json
{
  "event_id": "string",
  "success": true,
  "message": "Page view tracked successfully"
}
```

### POST /api/v1/events/user-action

Track a user action event.

**Request Body:**
```json
{
  "event_id": "string",
  "user_id": "string",
  "session_id": "string",
  "page_url": "string",
  "action_type": "string",
  "action_data": "string",
  "event_time": "2025-05-02T14:30:45Z"
}
```

**Response:**
```json
{
  "event_id": "string",
  "success": true,
  "message": "User action tracked successfully"
}
```

## Analytics

### GET /api/v1/analytics/page-views

Get analytics data for page views.

**Query Parameters:**
- `start_date` (optional): Start date for analytics in ISO format (defaults to 30 days ago)
- `end_date` (optional): End date for analytics in ISO format (defaults to current time)

**Response:**
```json
{
  "total_views": 12345,
  "unique_visitors": 5678,
  "average_load_time": 1250.5,
  "views_by_day": {
    "2025-05-01": 1234,
    "2025-05-02": 2345
  },
  "top_pages": [
    {
      "page_url": "/products",
      "views": 5000,
      "unique_visitors": 3000,
      "avg_load_time": 1100.5
    }
  ],
  "top_referrers": [
    {
      "referrer": "https://google.com",
      "views": 2500
    }
  ],
  "top_countries": [
    {
      "country": "United States",
      "views": 4000,
      "unique_visitors": 2500
    }
  ]
}
```

### GET /api/v1/analytics/user-actions

Get analytics data for user actions.

**Query Parameters:**
- `start_date` (optional): Start date for analytics in ISO format (defaults to 30 days ago)
- `end_date` (optional): End date for analytics in ISO format (defaults to current time)

**Response:**
```json
{
  "total_actions": 7890,
  "actions_by_type": {
    "click": 5000,
    "form_submit": 2000,
    "scroll": 890
  },
  "top_pages_with_actions": [
    {
      "page_url": "/checkout",
      "actions": 2000,
      "unique_users": 1500,
      "action_types": "click, form_submit"
    }
  ]
}
```

### POST /api/v1/analytics/funnel-analysis

Perform funnel analysis for a sequence of pages.

**Request Body:**
```json
{
  "funnel_steps": [
    "/",
    "/products/123",
    "/cart",
    "/checkout",
    "/order/confirmed"
  ],
  "start_date": "2025-04-02T00:00:00Z",
  "end_date": "2025-05-02T23:59:59Z"
}
```

**Response:**
```json
{
  "total_entered": 10000,
  "completed": 2000,
  "completion_rate": 20.0,
  "steps": [
    {
      "step": 1,
      "page_url": "/",
      "users": 10000,
      "conversion_rate": 100.0
    },
    {
      "step": 2,
      "page_url": "/products/123",
      "users": 7500,
      "conversion_rate": 75.0
    },
    {
      "step": 3,
      "page_url": "/cart",
      "users": 5000,
      "conversion_rate": 66.7
    },
    {
      "step": 4,
      "page_url": "/checkout",
      "users": 3000,
      "conversion_rate": 60.0
    },
    {
      "step": 5,
      "page_url": "/order/confirmed",
      "users": 2000,
      "conversion_rate": 66.7
    }
  ]
}
```

### GET /api/v1/analytics/retention

Analyze user retention over time periods.

**Query Parameters:**
- `start_date` (optional): Start date for cohort analysis in ISO format (defaults to 90 days ago)
- `end_date` (optional): End date for cohort analysis in ISO format (defaults to current time)
- `interval_days` (optional): Interval in days for cohort grouping (default: 7 for weekly cohorts)

**Response:**
```json
{
  "status": "not_implemented",
  "message": "Retention analysis endpoint is defined but not yet implemented"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

Returned when the request contains invalid data.

```json
{
  "detail": "Error message describing the validation issue"
}
```

### 500 Internal Server Error

Returned when an unexpected error occurs on the server.

```json
{
  "detail": "Error message describing the issue"
}
```

## Using the API with cURL

### Track a Page View

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/events/page-view' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_id": "test-event-001",
    "user_id": "test-user-001",
    "session_id": "test-session-001",
    "page_url": "/test-page",
    "referrer": "https://google.com",
    "user_agent": "Mozilla/5.0",
    "country": "United States",
    "event_time": "2025-05-02T14:30:45Z",
    "load_time": 1200
  }'
```

### Get Page Views Analytics

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/analytics/page-views?start_date=2025-04-02T00:00:00Z&end_date=2025-05-02T23:59:59Z'
```

### Perform Funnel Analysis

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/analytics/funnel-analysis' \
  -H 'Content-Type: application/json' \
  -d '{
    "funnel_steps": [
      "/",
      "/products/123",
      "/cart",
      "/checkout",
      "/order/confirmed"
    ],
    "start_date": "2025-04-02T00:00:00Z",
    "end_date": "2025-05-02T23:59:59Z"
  }'
```