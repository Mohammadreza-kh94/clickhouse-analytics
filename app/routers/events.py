from fastapi import APIRouter, HTTPException, status
from app.models.schemas import PageView, UserAction, PageViewResponse, UserActionResponse
from app.services import events_service

router = APIRouter(
    prefix="/events",
    tags=["events"],
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


@router.post(
    "/page-view",
    response_model=PageViewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Track page view event",
    description="""
    Tracks a page view event in ClickHouse.

    This endpoint stores information about a user's visit to a specific page, including:
    - User identification (user_id, session_id)
    - Page information (page_url, referrer)
    - Technical details (user_agent, load_time)
    - Geographic information (country, city)
    - Device information (device_type, browser, OS)

    The data is stored in the page_views table in ClickHouse, which is optimized for
    analytical queries using the MergeTree engine.
    """
)
async def track_page_view(page_view: PageView):
    """
    Track a page view event
    """
    try:
        event_id = events_service.insert_page_view(page_view)
        return PageViewResponse(
            event_id=event_id,
            success=True,
            message="Page view tracked successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to track page view: {str(e)}"
        )


@router.post(
    "/user-action",
    response_model=UserActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Track user action event",
    description="""
    Tracks a user action event in ClickHouse.

    This endpoint stores information about a user's interaction with the website, such as:
    - Clicks
    - Form submissions
    - Scrolling
    - Other interactions

    The action_type field indicates the type of action (e.g., "click", "form_submit"),
    and the action_data field can contain additional JSON data about the action.

    The data is stored in the user_actions table in ClickHouse, which is optimized for
    analytical queries using the MergeTree engine.
    """
)
async def track_user_action(user_action: UserAction):
    """
    Track a user action event
    """
    try:
        event_id = events_service.insert_user_action(user_action)
        return UserActionResponse(
            event_id=event_id,
            success=True,
            message="User action tracked successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to track user action: {str(e)}"
        )