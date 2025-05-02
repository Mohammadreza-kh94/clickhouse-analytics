from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PageView(BaseModel):
    """Schema for page view events"""
    event_id: str
    user_id: str
    session_id: str
    page_url: str
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    event_time: datetime = Field(default_factory=datetime.now)
    load_time: Optional[int] = None


class UserAction(BaseModel):
    """Schema for user action events"""
    event_id: str
    user_id: str
    session_id: str
    page_url: str
    action_type: str  # click, scroll, form_submit, etc.
    action_data: Optional[str] = None  # JSON string with action details
    event_time: datetime = Field(default_factory=datetime.now)


class PageViewResponse(BaseModel):
    """Response schema for tracked page view"""
    event_id: str
    success: bool
    message: str = "Page view tracked successfully"


class UserActionResponse(BaseModel):
    """Response schema for tracked user action"""
    event_id: str
    success: bool
    message: str = "User action tracked successfully"


class DateRangeParams(BaseModel):
    """Parameters for date range filtering"""
    start_date: datetime
    end_date: datetime = Field(default_factory=datetime.now)


class PageViewsAnalytics(BaseModel):
    """Schema for page views analytics results"""
    total_views: int
    unique_visitors: int
    average_load_time: float
    views_by_day: Dict[str, int]
    top_pages: List[Dict[str, Any]]
    top_referrers: List[Dict[str, Any]]
    top_countries: List[Dict[str, Any]]


class UserActionsAnalytics(BaseModel):
    """Schema for user actions analytics results"""
    total_actions: int
    actions_by_type: Dict[str, int]
    top_pages_with_actions: List[Dict[str, Any]]