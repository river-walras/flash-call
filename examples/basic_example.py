"""Basic example demonstrating how to use flash-call SDK.

This example shows:
1. Reading integration key from environment variable
2. Sending different types of alerts (Warning, Critical, Info)
3. Sending a recovery event (Ok)
"""

import os
import sys
from flash_call import set_key, push_alert
from dotenv import load_dotenv

load_dotenv()

def main():
    # Read integration key from environment variable
    integration_key = os.getenv("FLASHDUTY_INTEGRATION_KEY")

    if not integration_key:
        print("Error: FLASHDUTY_INTEGRATION_KEY environment variable not set")
        print("Please set it using: export FLASHDUTY_INTEGRATION_KEY=your-key-here")
        sys.exit(1)

    # Set the integration key globally
    set_key(integration_key)
    print(f"Integration key set: {integration_key[:20]}...")

    # # Example 1: Send a Warning alert
    print("\n1. Sending Warning alert...")
    response = push_alert(
        title_rule="cpu idle low than 20%",
        event_status="Warning",
        description="CPU usage is high on production server",
        labels={
            "service": "engine",
            "cluster": "nj",
            "resource": "es.nj.01",
            "check": "cpu.idle<20%",
            "metric": "node_cpu_seconds_total"
        }
    )
    print(f"   ✓ Alert created successfully")
    print(f"   Request ID: {response['request_id']}")
    print(f"   Alert Key: {response['data']['alert_key']}")

    # Save alert key for recovery
    alert_key_warning = response['data']['alert_key']

    # Example 2: Send a Critical alert
    print("\n2. Sending Critical alert...")
    response = push_alert(
        title_rule="Database connection pool exhausted",
        event_status="Critical",
        description="All database connections are in use, new requests are being rejected",
        labels={
            "service": "database",
            "cluster": "nj",
            "resource": "postgres-01",
            "check": "connection_pool_usage>95%"
        }
    )
    print(f"   ✓ Alert created successfully")
    print(f"   Request ID: {response['request_id']}")
    print(f"   Alert Key: {response['data']['alert_key']}")

    alert_key_critical = response['data']['alert_key']

    # Example 3: Send an Info alert
    print("\n3. Sending Info alert...")
    response = push_alert(
        title_rule="Scheduled maintenance window starting",
        event_status="Info",
        description="Database maintenance will begin in 10 minutes",
        labels={
            "service": "database",
            "cluster": "nj",
            "type": "maintenance"
        }
    )
    print(f"   ✓ Alert created successfully")
    print(f"   Request ID: {response['request_id']}")
    print(f"   Alert Key: {response['data']['alert_key']}")

    # Example 4: Send recovery events (Ok status)
    print("\n4. Sending recovery events...")

    # Recover the warning alert
    response = push_alert(
        title_rule="cpu idle recovered",
        event_status="Ok",
        alert_key=alert_key_warning,
        description="CPU usage has returned to normal levels",
        labels={
            "service": "engine",
            "cluster": "nj",
            "resource": "es.nj.01"
        }
    )
    print(f"   ✓ Warning alert recovered")
    print(f"   Request ID: {response['request_id']}")

    # Recover the critical alert
    response = push_alert(
        title_rule="Database connection pool recovered",
        event_status="Ok",
        alert_key=alert_key_critical,
        description="Connection pool has available connections",
        labels={
            "service": "database",
            "cluster": "nj",
            "resource": "postgres-01"
        }
    )
    print(f"   ✓ Critical alert recovered")
    print(f"   Request ID: {response['request_id']}")

    print("\n✅ All examples completed successfully!")


if __name__ == "__main__":
    main()
