"""Flashduty Alert Push SDK

A Python SDK for pushing alert events to Flashduty using standard HTTP protocol.
Supports both synchronous and asynchronous operations.
"""

from typing import Dict, List, Literal, Optional, TypedDict
import httpx


# Type definitions
EventStatus = Literal["Critical", "Warning", "Info", "Ok"]


class Image(TypedDict, total=False):
    """Image structure for alert notifications."""
    alt: str
    src: str
    href: str


class AlertData(TypedDict, total=False):
    """Response data structure."""
    alert_key: str


class ErrorResponse(TypedDict):
    """Error response structure."""
    code: str
    message: str


class SuccessResponse(TypedDict):
    """Success response structure."""
    request_id: str
    data: AlertData


class ErrorResponseFull(TypedDict):
    """Full error response structure."""
    request_id: str
    error: ErrorResponse


# Global integration key storage
_integration_key: Optional[str] = None
_user: Optional[str] = None

# Base URL for Flashduty API
BASE_URL = "https://api.flashcat.cloud/event/push/alert/standard"


def set_key(key: str, user: Optional[str] = None) -> None:
    """Set the global integration key for Flashduty API.

    Args:
        key: The integration key obtained from Flashduty after adding integration.
        user: Optional user identifier to prepend to alert titles.

    Example:
        >>> set_key("5c4cfe6e1ae15dfeb73bfc70181f786b073", user="admin")
    """
    global _integration_key, _user
    _integration_key = key
    _user = user


def get_key() -> Optional[str]:
    """Get the current integration key.

    Returns:
        The current integration key or None if not set.
    """
    return _integration_key


def get_user() -> Optional[str]:
    """Get the current user identifier.

    Returns:
        The current user identifier or None if not set.
    """
    return _user


def push_alert(
    title_rule: str,
    event_status: EventStatus,
    alert_key: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    images: Optional[List[Image]] = None,
    integration_key: Optional[str] = None,
) -> SuccessResponse:
    """Push an alert event to Flashduty (synchronous version).

    Args:
        title_rule: Alert title, max 512 characters.
        event_status: Alert status - "Critical", "Warning", "Info", or "Ok".
        alert_key: Optional alert identifier for updating existing alerts or recovery.
        description: Optional alert description, max 2048 characters.
        labels: Optional dict of labels (max 50 labels, key max 128 chars, value max 2048 chars).
        images: Optional list of images for notifications.
        integration_key: Optional integration key, uses global key if not provided.

    Returns:
        SuccessResponse with request_id and alert_key.

    Raises:
        ValueError: If no integration key is set or provided.
        httpx.HTTPStatusError: If the API returns an error status code.

    Example:
        >>> set_key("your-integration-key")
        >>> response = push_alert(
        ...     title_rule="cpu idle low than 20%",
        ...     event_status="Warning",
        ...     labels={
        ...         "service": "engine",
        ...         "cluster": "nj",
        ...         "resource": "es.nj.01",
        ...         "check": "cpu.idle<20%",
        ...         "metric": "node_cpu_seconds_total"
        ...     }
        ... )
        >>> print(response["data"]["alert_key"])
    """
    key = integration_key or _integration_key
    if not key:
        raise ValueError("Integration key must be set using set_key() or provided as parameter")

    # Prepend user to title_rule if set
    if _user is not None:
        title_rule = f"{_user} {title_rule}"

    # Build payload
    payload: Dict = {
        "title_rule": title_rule,
        "event_status": event_status,
    }

    if alert_key is not None:
        payload["alert_key"] = alert_key
    if description is not None:
        payload["description"] = description
    if labels is not None:
        payload["labels"] = labels
    if images is not None:
        payload["images"] = images

    # Make request
    with httpx.Client() as client:
        response = client.post(
            BASE_URL,
            params={"integration_key": key},
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()


async def push_alert_async(
    title_rule: str,
    event_status: EventStatus,
    alert_key: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    images: Optional[List[Image]] = None,
    integration_key: Optional[str] = None,
) -> SuccessResponse:
    """Push an alert event to Flashduty (asynchronous version).

    Args:
        title_rule: Alert title, max 512 characters.
        event_status: Alert status - "Critical", "Warning", "Info", or "Ok".
        alert_key: Optional alert identifier for updating existing alerts or recovery.
        description: Optional alert description, max 2048 characters.
        labels: Optional dict of labels (max 50 labels, key max 128 chars, value max 2048 chars).
        images: Optional list of images for notifications.
        integration_key: Optional integration key, uses global key if not provided.

    Returns:
        SuccessResponse with request_id and alert_key.

    Raises:
        ValueError: If no integration key is set or provided.
        httpx.HTTPStatusError: If the API returns an error status code.

    Example:
        >>> import asyncio
        >>> set_key("your-integration-key")
        >>> async def main():
        ...     response = await push_alert_async(
        ...         title_rule="cpu idle low than 20%",
        ...         event_status="Warning",
        ...         labels={
        ...             "service": "engine",
        ...             "cluster": "nj",
        ...             "resource": "es.nj.01"
        ...         }
        ...     )
        ...     print(response["data"]["alert_key"])
        >>> asyncio.run(main())
    """
    key = integration_key or _integration_key
    if not key:
        raise ValueError("Integration key must be set using set_key() or provided as parameter")

    # Prepend user to title_rule if set
    if _user is not None:
        title_rule = f"{_user} {title_rule}"

    # Build payload
    payload: Dict = {
        "title_rule": title_rule,
        "event_status": event_status,
    }

    if alert_key is not None:
        payload["alert_key"] = alert_key
    if description is not None:
        payload["description"] = description
    if labels is not None:
        payload["labels"] = labels
    if images is not None:
        payload["images"] = images

    # Make request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            BASE_URL,
            params={"integration_key": key},
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()


# Public API
__all__ = [
    "set_key",
    "get_key",
    "get_user",
    "push_alert",
    "push_alert_async",
    "EventStatus",
    "Image",
    "AlertData",
    "SuccessResponse",
    "ErrorResponse",
    "ErrorResponseFull",
]