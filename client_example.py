"""
This script demonstrates how to use the ClickHouse Analytics API
to track events and retrieve analytics data.
"""
import requests
import uuid
import json
from datetime import datetime, timedelta

# Base URL for API
BASE_URL = "http://localhost:8000/api/v1"


def generate_uuid():
    """Generate a unique ID for events."""
    return str(uuid.uuid4())


def track_page_view(user_id, session_id, page_url, **kwargs):
    """
    Track a page view event

    Args:
        user_id: ID of the user
        session_id: ID of the session
        page_url: URL of the viewed page
        **kwargs: Additional page view data
    """
    # Prepare page view data
    page_view_data = {
        "event_id": generate_uuid(),
        "user_id": user_id,
        "session_id": session_id,
        "page_url": page_url,
        "event_time": datetime.now().isoformat(),
        **kwargs
    }

    # Send request to track page view
    response = requests.post(
        f"{BASE_URL}/events/page-view",
        json=page_view_data
    )

    if response.status_code == 200:
        print(f"Page view tracked: {response.json()}")
    else:
        print(f"Failed to track page view: {response.text}")

    return response.json() if response.status_code == 200 else None


def track_user_action(user_id, session_id, page_url, action_type, action_data=None):
    """
    Track a user action event

    Args:
        user_id: ID of the user
        session_id: ID of the session
        page_url: URL where the action occurred
        action_type: Type of action (e.g., 'click', 'form_submit')
        action_data: Additional data about the action
    """
    # Prepare user action data
    user_action_data = {
        "event_id": generate_uuid(),
        "user_id": user_id,
        "session_id": session_id,
        "page_url": page_url,
        "action_type": action_type,
        "action_data": json.dumps(action_data) if action_data else None,
        "event_time": datetime.now().isoformat()
    }

    # Send request to track user action
    response = requests.post(
        f"{BASE_URL}/events/user-action",
        json=user_action_data
    )

    if response.status_code == 200:
        print(f"User action tracked: {response.json()}")
    else:
        print(f"Failed to track user action: {response.text}")

    return response.json() if response.status_code == 200 else None


def get_page_views_analytics(days=30):
    """
    Get page views analytics for the last N days

    Args:
        days: Number of days to look back
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Format dates for URL parameters
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    # Send request to get page views analytics
    response = requests.get(
        f"{BASE_URL}/analytics/page-views",
        params={
            "start_date": start_date_str,
            "end_date": end_date_str
        }
    )

    if response.status_code == 200:
        print("Page Views Analytics:")
        analytics = response.json()
        print(f"Total Views: {analytics['total_views']}")
        print(f"Unique Visitors: {analytics['unique_visitors']}")
        print(f"Average Load Time: {analytics['average_load_time']} ms")

        print("\nTop Pages:")
        for page in analytics["top_pages"]:
            print(f"  {page['page_url']}: {page['views']} views")
    else:
        print(f"Failed to get page views analytics: {response.text}")

    return response.json() if response.status_code == 200 else None


def get_user_actions_analytics(days=30):
    """
    Get user actions analytics for the last N days

    Args:
        days: Number of days to look back
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Format dates for URL parameters
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    # Send request to get user actions analytics
    response = requests.get(
        f"{BASE_URL}/analytics/user-actions",
        params={
            "start_date": start_date_str,
            "end_date": end_date_str
        }
    )

    if response.status_code == 200:
        print("User Actions Analytics:")
        analytics = response.json()
        print(f"Total Actions: {analytics['total_actions']}")

        print("\nActions by Type:")
        for action_type, count in analytics["actions_by_type"].items():
            print(f"  {action_type}: {count}")

        print("\nTop Pages with Actions:")
        for page in analytics["top_pages_with_actions"]:
            print(f"  {page['page_url']}: {page['actions']} actions by {page['unique_users']} users")
    else:
        print(f"Failed to get user actions analytics: {response.text}")

    return response.json() if response.status_code == 200 else None


def analyze_funnel(funnel_steps, days=30):
    """
    Perform funnel analysis for a sequence of pages

    Args:
        funnel_steps: List of page URLs representing steps in the funnel
        days: Number of days to look back
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Format dates for URL parameters
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    # Send request to perform funnel analysis
    response = requests.post(
        f"{BASE_URL}/analytics/funnel-analysis",
        json={
            "funnel_steps": funnel_steps,
            "start_date": start_date_str,
            "end_date": end_date_str
        }
    )

    if response.status_code == 200:
        print("Funnel Analysis:")
        funnel = response.json()
        print(f"Total Entered: {funnel['total_entered']}")
        print(f"Completed: {funnel['completed']}")
        print(f"Completion Rate: {funnel['completion_rate']}%")

        print("\nSteps:")
        for step in funnel["steps"]:
            print(
                f"  Step {step['step']}: {step['page_url']} - {step['users']} users ({step['conversion_rate']}% conversion)")
    else:
        print(f"Failed to perform funnel analysis: {response.text}")

    return response.json() if response.status_code == 200 else None


def simulate_user_journey():
    """Simulate a user journey with multiple events."""
    # Generate unique IDs
    user_id = f"user_{generate_uuid().split('-')[0]}"
    session_id = f"session_{generate_uuid().split('-')[0]}"

    # Simulate page views and actions for a checkout flow

    # Home page
    track_page_view(
        user_id=user_id,
        session_id=session_id,
        page_url="/",
        referrer="https://google.com",
        load_time=850
    )

    track_user_action(
        user_id=user_id,
        session_id=session_id,
        page_url="/",
        action_type="click",
        action_data={"element": "featured_product", "product_id": "prod123"}
    )

    # Product page
    track_page_view(
        user_id=user_id,
        session_id=session_id,
        page_url="/products/prod123",
        referrer="/",
        load_time=920
    )

    track_user_action(
        user_id=user_id,
        session_id=session_id,
        page_url="/products/prod123",
        action_type="click",
        action_data={"element": "add_to_cart", "product_id": "prod123"}
    )

    # Cart page
    track_page_view(
        user_id=user_id,
        session_id=session_id,
        page_url="/cart",
        referrer="/products/prod123",
        load_time=780
    )

    track_user_action(
        user_id=user_id,
        session_id=session_id,
        page_url="/cart",
        action_type="click",
        action_data={"element": "checkout_button"}
    )

    # Checkout page
    track_page_view(
        user_id=user_id,
        session_id=session_id,
        page_url="/checkout",
        referrer="/cart",
        load_time=1050
    )

    track_user_action(
        user_id=user_id,
        session_id=session_id,
        page_url="/checkout",
        action_type="form_submit",
        action_data={"form": "shipping_info"}
    )

    # Order confirmation
    track_page_view(
        user_id=user_id,
        session_id=session_id,
        page_url="/order/confirmed",
        referrer="/checkout",
        load_time=650
    )

    print(f"Simulated journey for user {user_id} completed")


if __name__ == "__main__":
    # Simulate multiple user journeys
    for _ in range(3):
        simulate_user_journey()

    # Get analytics
    get_page_views_analytics(days=1)
    get_user_actions_analytics(days=1)

    # Analyze checkout funnel
    checkout_funnel = ["/", "/products/prod123", "/cart", "/checkout", "/order/confirmed"]
    analyze_funnel(checkout_funnel, days=1)