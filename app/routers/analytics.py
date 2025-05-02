from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status, Body

from app.models.schemas import PageViewsAnalytics, UserActionsAnalytics, DateRangeParams
from app.services import analytics_service

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to process the request"}
                }
            }
        }
    }
)


@router.get(
    "/page-views",
    response_model=PageViewsAnalytics,
    summary="Get page views analytics",
    description="""
    Retrieves analytics data for page views within a specified date range.

    This endpoint demonstrates ClickHouse's OLAP capabilities by:
    - Aggregating total page views and unique visitors
    - Calculating average load times
    - Grouping views by day for time-series analysis
    - Identifying top pages by traffic
    - Analyzing referrer sources
    - Breaking down traffic by country

    The query leverages ClickHouse's columnar storage and aggregation functions
    to perform these calculations efficiently over large datasets.
    """
)
async def get_page_views_analytics(
        start_date: Optional[datetime] = Query(
            None,
            description="Start date for analytics (defaults to 30 days ago)",
            example="2025-04-02T00:00:00Z"
        ),
        end_date: Optional[datetime] = Query(
            None,
            description="End date for analytics (defaults to current time)",
            example="2025-05-02T23:59:59Z"
        )
):
    """
    Get analytics data for page views

    If start_date is not provided, defaults to 30 days ago
    If end_date is not provided, defaults to current time
    """
    # Default to last 30 days if dates not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    try:
        return analytics_service.get_page_views_analytics(start_date, end_date)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve page views analytics: {str(e)}"
        )


@router.get(
    "/user-actions",
    response_model=UserActionsAnalytics,
    summary="Get user actions analytics",
    description="""
    Retrieves analytics data for user actions within a specified date range.

    This endpoint provides insights into user behavior by:
    - Calculating total actions performed
    - Breaking down actions by type (click, form_submit, etc.)
    - Identifying pages with the most user interactions

    The query demonstrates ClickHouse's ability to efficiently process and analyze
    event data from the user_actions table.
    """
)
async def get_user_actions_analytics(
        start_date: Optional[datetime] = Query(
            None,
            description="Start date for analytics (defaults to 30 days ago)",
            example="2025-04-02T00:00:00Z"
        ),
        end_date: Optional[datetime] = Query(
            None,
            description="End date for analytics (defaults to current time)",
            example="2025-05-02T23:59:59Z"
        )
):
    """
    Get analytics data for user actions

    If start_date is not provided, defaults to 30 days ago
    If end_date is not provided, defaults to current time
    """
    # Default to last 30 days if dates not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    try:
        return analytics_service.get_user_actions_analytics(start_date, end_date)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user actions analytics: {str(e)}"
        )


@router.post(
    "/funnel-analysis",
    summary="Perform funnel analysis",
    description="""
    Performs a funnel analysis for a sequence of pages within a specified date range.

    This endpoint demonstrates advanced OLAP capabilities by:
    - Tracking user progression through a defined sequence of steps
    - Calculating conversion rates between steps
    - Identifying drop-off points in the user journey

    The funnel analysis is useful for analyzing user flows such as checkout processes,
    registration flows, or other multi-step user journeys.

    ClickHouse's ability to efficiently query large datasets makes it ideal for
    this type of analysis, which would be computationally expensive in traditional
    OLTP databases.
    """
)
async def get_funnel_analysis(
        funnel_steps: List[str] = Body(
            ...,
            description="List of page URLs representing steps in the funnel",
            example=["/", "/products/123", "/cart", "/checkout", "/order/confirmed"]
        ),
        start_date: Optional[datetime] = Body(
            None,
            description="Start date for analysis (defaults to 30 days ago)",
            example="2025-04-02T00:00:00Z"
        ),
        end_date: Optional[datetime] = Body(
            None,
            description="End date for analysis (defaults to current time)",
            example="2025-05-02T23:59:59Z"
        )
) -> Dict[str, Any]:
    """
    Perform funnel analysis for a sequence of pages

    Args:
        funnel_steps: List of page URLs representing steps in the funnel
        start_date: Start date for analysis (defaults to 30 days ago)
        end_date: End date for analysis (defaults to current time)
    """
    # Default to last 30 days if dates not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    if not funnel_steps or len(funnel_steps) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Funnel analysis requires at least 2 steps"
        )

    try:
        return analytics_service.get_funnel_analysis(start_date, end_date, funnel_steps)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform funnel analysis: {str(e)}"
        )


@router.get(
    "/retention",
    summary="Analyze user retention",
    description="""
    Analyzes user retention over time periods.

    This endpoint demonstrates how ClickHouse can be used for cohort analysis:
    - Tracking which users return over different time periods
    - Calculating retention rates for different user cohorts
    - Identifying trends in user engagement over time

    The analysis leverages ClickHouse's efficient handling of time-series data
    and user identifiers to calculate retention metrics.
    """
)
async def analyze_retention(
        start_date: Optional[datetime] = Query(
            None,
            description="Start date for cohort analysis (defaults to 90 days ago)",
            example="2025-02-02T00:00:00Z"
        ),
        end_date: Optional[datetime] = Query(
            None,
            description="End date for cohort analysis (defaults to current time)",
            example="2025-05-02T23:59:59Z"
        ),
        interval_days: int = Query(
            7,
            description="Interval in days for cohort grouping (default: 7 for weekly cohorts)",
            ge=1,
            le=90
        )
) -> Dict[str, Any]:
    """
    Analyze user retention over time periods

    Args:
        start_date: Start date for cohort analysis (defaults to 90 days ago)
        end_date: End date for cohort analysis (defaults to current time)
        interval_days: Interval in days for cohort grouping (default: 7 for weekly cohorts)
    """
    # Default to last 90 days if dates not provided (retention needs more data)
    if not start_date:
        start_date = datetime.now() - timedelta(days=90)
    if not end_date:
        end_date = datetime.now()

    try:
        # This endpoint would use a method like analytics_service.analyze_retention()
        # For now, return a placeholder response
        return {
            "status": "not_implemented",
            "message": "Retention analysis endpoint is defined but not yet implemented"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze user retention: {str(e)}"
        )