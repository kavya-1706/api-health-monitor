import time
from datetime import datetime, timezone
import requests


# Checks the availability and response time of an API and classifies it as UP, DEGRADED, DOWN
# Records the HTTP status code, response time, timestamp, and any errors
# Runs checks for all enabled services, saves the results to the database, and returns them

# UP- Expected HTTP status and acceptable response time
# DEGRADED- Unexpected HTTP status/Response exceeds the slow threshold
# DOWN- Timeout or other Requests exception

def check_api(
    url,
    expected_status=200,
    timeout=5.0,
    slow_threshold_ms=1500.0,
):
    started = time.perf_counter()
    checked_at = datetime.now(timezone.utc).isoformat()

    try:
        response = requests.get(url, timeout=timeout)
        elapsed_ms = round(
            (time.perf_counter() - started) * 1000, 2
        )
        if response.status_code != expected_status:
            status = "DEGRADED"
            error = (
                f"Expected HTTP {expected_status}, "
                f"got HTTP {response.status_code}"
            )
        elif elapsed_ms > slow_threshold_ms:
            status = "DEGRADED"
            error = "Response time exceeded the slow threshold"
        else:
            status = "UP"
            error = None

        return {
            "url": url,
            "checked_at": checked_at,
            "status": status,
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
            "error": error,
        }

    except requests.exceptions.Timeout:
        return {
            "url": url,
            "checked_at": checked_at,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": None,
            "error": f"Request timed out after {timeout} seconds",
        }

    except requests.exceptions.RequestException as exc:
        return {
            "url": url,
            "checked_at": checked_at,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def run_all_checks():

    from flask import current_app
    from app.database import get_db, save_check_result
    from config import SLOW_RESPONSE_MS

    db = get_db()
    services = db.execute(
        "SELECT * FROM services WHERE enabled = 1 ORDER BY id"
    ).fetchall()

    results = []
    for service in services:
        result = check_api(
            service["url"],
            expected_status=service["expected_status"],
            timeout=service["timeout_seconds"],
            slow_threshold_ms=current_app.config.get(
                "SLOW_RESPONSE_MS", SLOW_RESPONSE_MS
            ),
        )
        save_check_result(service["id"], result)
        results.append(result)

    return results
