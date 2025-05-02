from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import uvicorn
import atexit
import os

from app.config import API_PREFIX
from app.database import init_database, close_connection
from app.routers import events, analytics

# Get environment variables
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Initialize FastAPI app
app = FastAPI(
    title="ClickHouse Analytics API",
    description="""
    API for tracking and analyzing website events using ClickHouse as an OLAP database.

    ## Features

    * **Event Tracking**: Track page views and user actions
    * **Analytics**: Get insights from tracked events
    * **Funnel Analysis**: Analyze user conversion through predefined steps

    ## About ClickHouse

    ClickHouse is an open-source, column-oriented database management system that allows 
    for real-time analytics using SQL queries. It's designed for OLAP (Online Analytical 
    Processing) workloads, making it ideal for this analytics application.
    """,
    version="1.0.0",
    docs_url=None,  # Disable the default docs
    redoc_url=None,  # Disable the default redoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(events.router, prefix=API_PREFIX)
app.include_router(analytics.router, prefix=API_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    init_database()
    print("ClickHouse Analytics API started")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    close_connection()
    print("ClickHouse Analytics API shutdown")


# Register the close_connection function to be called on exit
atexit.register(close_connection)


@app.get("/", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "ClickHouse Analytics API is running"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with improved styling"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="/favicon.ico",
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    """Custom OpenAPI schema with enhanced metadata"""
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=SERVER_HOST, port=SERVER_PORT, reload=DEBUG)