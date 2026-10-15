import os

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH =os.environ.get(
    "API_MONITOR_DATABASE",
    os.path.join(BASE_DIR, "api_monitor.db"),
)
CHECK_INTERVAL_SECONDS=int(
    os.environ.get("CHECK_INTERVAL_SECONDS", "60")
)
DEFAULT_TIMEOUT_SECONDS=float(
    os.environ.get("DEFAULT_TIMEOUT_SECONDS", "5")
)
SLOW_RESPONSE_MS=float(
    os.environ.get("SLOW_RESPONSE_MS", "1500")
)
