from datetime import datetime
from typing import Dict, List, Any

from app.database import get_clickhouse_client
from app.models.schemas import PageViewsAnalytics, UserActionsAnalytics


def get_page_views_analytics(start_date: datetime, end_date: datetime) -> PageViewsAnalytics:
    """
    Get analytics data for page views within a date range

    Args:
        start_date: Start date for analytics
        end_date: End date for analytics

    Returns:
        PageViewsAnalytics object with aggregated data
    """
    client = get_clickhouse_client()

    # Format dates for ClickHouse queries
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    # Get total page views
    total_views_query = f"""
    SELECT COUNT(*) as total
    FROM page_views
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    """
    total_views_result = client.query(total_views_query)
    total_views = total_views_result.result_rows[0][0] if total_views_result.result_rows else 0

    # Get unique visitors
    unique_visitors_query = f"""
    SELECT COUNT(DISTINCT user_id) as unique_users
    FROM page_views
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    """
    unique_visitors_result = client.query(unique_visitors_query)
    unique_visitors = unique_visitors_result.result_rows[0][0] if unique_visitors_result.result_rows else 0

    # Get average load time
    avg_load_time_query = f"""
    SELECT AVG(load_time) as avg_load_time
    FROM page_views
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    """
    avg_load_time_result = client.query(avg_load_time_query)
    average_load_time = avg_load_time_result.result_rows[0][0] if avg_load_time_result.result_rows else 0

    # Get views by day
    views_by_day_query = f"""
    SELECT 
        toDate(event_time) as day,
        COUNT(*) as views
    FROM page_views
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    GROUP BY day
    ORDER BY day
    """
    views_by_day_result = client.query(views_by_day_query)
    views_by_day = {row[0].strftime('%Y-%m-%d'): row[1] for row in views_by_day_result.result_rows}

    # Get top pages
    top_pages_query = f"""
    SELECT 
        page_url,
        COUNT(*) as views,
        COUNT(DISTINCT user_id) as unique_visitors,
        AVG(load_time) as avg_load_time
    FROM page_views
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    GROUP BY page_url
    ORDER BY views DESC
    LIMIT 10
    """
    top_pages_result = client.query(top_pages_query)
    top_pages = [
        {
            'page_url': row[0],
            'views': row[1],
            'unique_visitors': row[2],
            'avg_load_time': row[3]
        }
        for row in top_pages_result.result_rows
    ]

    # Get top referrers
    top_referrers_query = f"""
    SELECT 
        referrer,
        COUNT(*) as views
    FROM page_views
    WHERE 
        event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
        AND referrer != ''
    GROUP BY referrer
    ORDER BY views DESC
    LIMIT 10
    """
    top_referrers_result = client.query(top_referrers_query)
    top_referrers = [
        {
            'referrer': row[0],
            'views': row[1]
        }
        for row in top_referrers_result.result_rows
    ]

    # Get top countries
    top_countries_query = f"""
    SELECT 
        country,
        COUNT(*) as views,
        COUNT(DISTINCT user_id) as unique_visitors
    FROM page_views
    WHERE 
        event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
        AND country != ''
    GROUP BY country
    ORDER BY views DESC
    LIMIT 10
    """
    top_countries_result = client.query(top_countries_query)
    top_countries = [
        {
            'country': row[0],
            'views': row[1],
            'unique_visitors': row[2]
        }
        for row in top_countries_result.result_rows
    ]

    return PageViewsAnalytics(
        total_views=total_views,
        unique_visitors=unique_visitors,
        average_load_time=average_load_time,
        views_by_day=views_by_day,
        top_pages=top_pages,
        top_referrers=top_referrers,
        top_countries=top_countries
    )


def get_user_actions_analytics(start_date: datetime, end_date: datetime) -> UserActionsAnalytics:
    """
    Get analytics data for user actions within a date range

    Args:
        start_date: Start date for analytics
        end_date: End date for analytics

    Returns:
        UserActionsAnalytics object with aggregated data
    """
    client = get_clickhouse_client()

    # Format dates for ClickHouse queries
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    # Get total actions
    total_actions_query = f"""
    SELECT COUNT(*) as total
    FROM user_actions
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    """
    total_actions_result = client.query(total_actions_query)
    total_actions = total_actions_result.result_rows[0][0] if total_actions_result.result_rows else 0

    # Get actions by type
    actions_by_type_query = f"""
    SELECT 
        action_type,
        COUNT(*) as count
    FROM user_actions
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    GROUP BY action_type
    ORDER BY count DESC
    """
    actions_by_type_result = client.query(actions_by_type_query)
    actions_by_type = {row[0]: row[1] for row in actions_by_type_result.result_rows}

    # Get top pages with actions
    top_pages_query = f"""
    SELECT 
        page_url,
        COUNT(*) as actions,
        COUNT(DISTINCT user_id) as unique_users,
        arrayStringConcat(groupArray(DISTINCT action_type), ', ') as action_types
    FROM user_actions
    WHERE event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
    GROUP BY page_url
    ORDER BY actions DESC
    LIMIT 10
    """
    top_pages_result = client.query(top_pages_query)
    top_pages_with_actions = [
        {
            'page_url': row[0],
            'actions': row[1],
            'unique_users': row[2],
            'action_types': row[3]
        }
        for row in top_pages_result.result_rows
    ]

    return UserActionsAnalytics(
        total_actions=total_actions,
        actions_by_type=actions_by_type,
        top_pages_with_actions=top_pages_with_actions
    )


def get_funnel_analysis(
        start_date: datetime,
        end_date: datetime,
        funnel_steps: List[str]
) -> Dict[str, Any]:
    """
    Perform funnel analysis to track user progression through a series of steps

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        funnel_steps: List of page URLs representing steps in the funnel

    Returns:
        Dictionary with funnel analysis results
    """
    client = get_clickhouse_client()

    # Format dates for ClickHouse queries
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    # Prepare steps for query
    steps_str = "','".join(funnel_steps)

    # Get total users who entered the funnel (first step)
    first_step_query = f"""
    SELECT COUNT(DISTINCT user_id) as users
    FROM page_views
    WHERE 
        event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
        AND page_url = '{funnel_steps[0]}'
    """
    first_step_result = client.query(first_step_query)
    users_entered = first_step_result.result_rows[0][0] if first_step_result.result_rows else 0

    # Get users at each step
    steps_data = []
    for i, step in enumerate(funnel_steps):
        step_query = f"""
        SELECT COUNT(DISTINCT user_id) as users
        FROM page_views
        WHERE 
            event_time BETWEEN '{start_date_str}' AND '{end_date_str}'
            AND page_url = '{step}'
        """
        step_result = client.query(step_query)
        users_at_step = step_result.result_rows[0][0] if step_result.result_rows else 0

        # Calculate conversion rate from previous step
        conversion_rate = 0
        if i == 0:
            conversion_rate = 100  # First step is always 100%
        else:
            previous_users = steps_data[i - 1]['users']
            conversion_rate = (users_at_step / previous_users * 100) if previous_users > 0 else 0

        steps_data.append({
            'step': i + 1,
            'page_url': step,
            'users': users_at_step,
            'conversion_rate': round(conversion_rate, 2)
        })

    # Calculate overall funnel conversion rate
    completion_rate = 0
    if users_entered > 0 and len(steps_data) > 0:
        completion_rate = steps_data[-1]['users'] / users_entered * 100

    return {
        'total_entered': users_entered,
        'completed': steps_data[-1]['users'] if steps_data else 0,
        'completion_rate': round(completion_rate, 2),
        'steps': steps_data
    }