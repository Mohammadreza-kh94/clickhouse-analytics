from app.database import get_clickhouse_client
from app.models.schemas import PageView, UserAction


def insert_page_view(page_view: PageView) -> str:
    """
    Insert a page view event into ClickHouse

    Args:
        page_view: The page view data to insert

    Returns:
        event_id: The ID of the inserted event
    """
    client = get_clickhouse_client()

    # Prepare data for insertion
    data = [
        [
            page_view.event_id,
            page_view.user_id,
            page_view.session_id,
            page_view.page_url,
            page_view.referrer or '',
            page_view.user_agent or '',
            page_view.ip_address or '',
            page_view.country or '',
            page_view.city or '',
            page_view.device_type or '',
            page_view.browser or '',
            page_view.os or '',
            page_view.event_time,
            page_view.load_time or 0
        ]
    ]

    # Insert data into page_views table
    client.insert(
        'page_views',
        data,
        column_names=[
            'event_id', 'user_id', 'session_id', 'page_url', 'referrer',
            'user_agent', 'ip_address', 'country', 'city', 'device_type',
            'browser', 'os', 'event_time', 'load_time'
        ]
    )

    return page_view.event_id


def insert_user_action(user_action: UserAction) -> str:
    """
    Insert a user action event into ClickHouse

    Args:
        user_action: The user action data to insert

    Returns:
        event_id: The ID of the inserted event
    """
    client = get_clickhouse_client()

    # Prepare data for insertion
    data = [
        [
            user_action.event_id,
            user_action.user_id,
            user_action.session_id,
            user_action.page_url,
            user_action.action_type,
            user_action.action_data or '',
            user_action.event_time
        ]
    ]

    # Insert data into user_actions table
    client.insert(
        'user_actions',
        data,
        column_names=[
            'event_id', 'user_id', 'session_id', 'page_url',
            'action_type', 'action_data', 'event_time'
        ]
    )

    return user_action.event_id