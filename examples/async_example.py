"""Async example demonstrating how to use flash-call SDK with asyncio.

This example shows:
1. Reading integration key from environment variable
2. Using async version of push_alert
3. Concurrent alert sending
"""

import asyncio
import os
import sys
from flash_call import set_key, push_alert_async


async def send_alert(title: str, status: str, labels: dict):
    """Helper function to send an alert asynchronously."""
    try:
        response = await push_alert_async(
            title_rule=title,
            event_status=status,
            labels=labels
        )
        print(f"✓ Alert sent: {title}")
        print(f"  Alert Key: {response['data']['alert_key']}")
        return response['data']['alert_key']
    except Exception as e:
        print(f"✗ Failed to send alert: {title}")
        print(f"  Error: {e}")
        return None


async def main():
    # Read integration key from environment variable
    integration_key = os.getenv("FLASHDUTY_INTEGRATION_KEY")

    if not integration_key:
        print("Error: FLASHDUTY_INTEGRATION_KEY environment variable not set")
        print("Please set it using: export FLASHDUTY_INTEGRATION_KEY=your-key-here")
        sys.exit(1)

    # Set the integration key globally
    set_key(integration_key)
    print(f"Integration key set: {integration_key[:20]}...")

    # Example 1: Send multiple alerts concurrently
    print("\n1. Sending multiple alerts concurrently...")

    tasks = [
        send_alert(
            "High CPU usage on server-01",
            "Warning",
            {"service": "web", "host": "server-01", "metric": "cpu"}
        ),
        send_alert(
            "High memory usage on server-02",
            "Warning",
            {"service": "web", "host": "server-02", "metric": "memory"}
        ),
        send_alert(
            "Disk space low on server-03",
            "Critical",
            {"service": "storage", "host": "server-03", "metric": "disk"}
        ),
    ]

    # Wait for all alerts to be sent concurrently
    alert_keys = await asyncio.gather(*tasks)
    print(f"\n   Sent {len([k for k in alert_keys if k])} alerts successfully")

    # Example 2: Send alert and then recovery
    print("\n2. Sending alert followed by recovery...")

    # Send critical alert
    response = await push_alert_async(
        title_rule="API latency exceeding threshold",
        event_status="Critical",
        description="API response time > 2000ms",
        labels={
            "service": "api",
            "endpoint": "/users",
            "metric": "latency"
        }
    )
    alert_key = response['data']['alert_key']
    print(f"   ✓ Critical alert sent: {alert_key}")

    # Simulate some time passing
    print("   Waiting 2 seconds...")
    await asyncio.sleep(2)

    # Send recovery
    response = await push_alert_async(
        title_rule="API latency recovered",
        event_status="Ok",
        alert_key=alert_key,
        description="API response time back to normal",
        labels={
            "service": "api",
            "endpoint": "/users"
        }
    )
    print(f"   ✓ Recovery event sent")

    # Example 3: Monitor multiple services
    print("\n3. Monitoring multiple services...")

    async def monitor_service(service_name: str, check_interval: int):
        """Simulate monitoring a service."""
        print(f"   Starting monitor for {service_name}")

        # Send initial status
        await push_alert_async(
            title_rule=f"{service_name} monitoring started",
            event_status="Info",
            labels={"service": service_name, "type": "monitoring"}
        )

        await asyncio.sleep(check_interval)

        print(f"   ✓ {service_name} check completed")

    # Monitor multiple services concurrently
    monitors = [
        monitor_service("web-service", 1),
        monitor_service("api-service", 1),
        monitor_service("db-service", 1),
    ]

    await asyncio.gather(*monitors)

    print("\n✅ All async examples completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
