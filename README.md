# flash-call

A Python SDK for pushing alert events to Flashduty using the standard HTTP protocol. Supports both synchronous and asynchronous operations.

## Features

- Simple and intuitive API
- Both sync and async support
- Type hints for better IDE support
- Global integration key management
- Full support for Flashduty standard alert protocol

## Installation

```bash
uv add flash-call
```

Or with pip:

```bash
pip install flash-call
```

## Quick Start

### Basic Usage (Sync)

```python
from flash_call import set_key, push_alert

# Set your integration key globally
set_key("your-integration-key-here")

# Push a warning alert
response = push_alert(
    title_rule="cpu idle low than 20%",
    event_status="Warning",
    labels={
        "service": "engine",
        "cluster": "nj",
        "resource": "es.nj.01",
        "check": "cpu.idle<20%",
        "metric": "node_cpu_seconds_total"
    }
)

print(f"Alert created with key: {response['data']['alert_key']}")
```

### Async Usage

```python
import asyncio
from flash_call import set_key, push_alert_async

async def main():
    set_key("your-integration-key-here")

    response = await push_alert_async(
        title_rule="High memory usage detected",
        event_status="Critical",
        description="Memory usage exceeded 90%",
        labels={
            "service": "database",
            "host": "db-01.example.com"
        }
    )

    print(f"Alert key: {response['data']['alert_key']}")

asyncio.run(main())
```

### Recovery Event

To close an alert, send a recovery event with status "Ok":

```python
from flash_call import push_alert

# Send recovery event
push_alert(
    title_rule="cpu idle recovered",
    event_status="Ok",
    alert_key="9qJ798NJoXS4UMVB5SHsNj",  # Use the alert_key from the original alert
    labels={
        "service": "engine",
        "cluster": "nj"
    }
)
```

## API Reference

### `set_key(api_key: str, user: str | None = None, strategy: str | None = None) -> None`

Set the global integration key for Flashduty API.

**Parameters:**
- `api_key`: The integration key obtained from Flashduty after adding integration
- `user` (optional): User identifier to attach to alert labels as `user_id`
- `strategy` (optional): Strategy identifier to attach to alert labels as `strategy_id`

### `push_alert(...) -> SuccessResponse`

Push an alert event to Flashduty (synchronous version).

**Parameters:**
- `title_rule` (str, required): Alert title, max 512 characters
- `event_status` (EventStatus, required): Alert status - "Critical", "Warning", "Info", or "Ok"
- `alert_key` (str, optional): Alert identifier for updating existing alerts or recovery
- `description` (str, optional): Alert description, max 2048 characters
- `labels` (dict, optional): Dictionary of labels (max 50 labels)
- `images` (list[Image], optional): List of images for notifications
- `integration_key` (str, optional): Integration key, uses global key if not provided

**Returns:**
- `SuccessResponse`: Dict containing `request_id` and `data` with `alert_key`

**Raises:**
- `ValueError`: If no integration key is set or provided
- `httpx.HTTPStatusError`: If the API returns an error status code

### `push_alert_async(...) -> SuccessResponse`

Push an alert event to Flashduty (asynchronous version).

Same parameters and return value as `push_alert()`, but returns a coroutine.

## Event Status

The SDK supports four event statuses:

- `"Critical"`: Severe alerts
- `"Warning"`: Warning alerts
- `"Info"`: Information alerts
- `"Ok"`: Recovery events (closes the alert)

## Labels Best Practices

Labels are key-value pairs that describe the alert. Good practices:

1. **Source information**: `host`, `cluster`, `check`, `metric`
2. **Ownership**: `team`, `owner`
3. **Classification**: `class` (api, db, net)
4. **Limits**: Max 50 labels, key max 128 chars, value max 2048 chars

Example:

```python
labels = {
    "service": "engine",
    "cluster": "nj",
    "resource": "es.nj.01",
    "check": "cpu.idle<20%",
    "metric": "node_cpu_seconds_total",
    "team": "platform",
    "severity": "high"
}
```

## Images

You can attach images to alerts for better visualization:

```python
from flash_call import push_alert

push_alert(
    title_rule="Service degradation detected",
    event_status="Warning",
    images=[
        {
            "alt": "Performance graph",
            "src": "https://example.com/graph.png",
            "href": "https://example.com/dashboard"
        }
    ]
)
```

## Error Handling

```python
from flash_call import push_alert
import httpx

try:
    response = push_alert(
        title_rule="Test alert",
        event_status="Info"
    )
except ValueError as e:
    print(f"Configuration error: {e}")
except httpx.HTTPStatusError as e:
    print(f"API error: {e.response.status_code}")
    error_data = e.response.json()
    print(f"Error code: {error_data['error']['code']}")
    print(f"Error message: {error_data['error']['message']}")
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for package management.

```bash
# Clone the repository
git clone https://github.com/yourusername/flash-call.git
cd flash-call

# Sync dependencies
uv sync

# Run tests (if available)
uv run pytest
```

## License

MIT License

## Links

- [Flashduty Official Documentation](https://docs.flashcat.cloud/)
- [Standard Alert Protocol](https://docs.flashcat.cloud/event/push/alert/standard)
