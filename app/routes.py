from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)

from app.database import (
    get_availability,
    get_recent_results,
    get_services_with_latest_results,
)
from app.monitor import run_all_checks


main = Blueprint("main", __name__)


@main.get("/")
def dashboard():
    services = get_services_with_latest_results()

    availability = {
        service["id"]: get_availability(service["id"])
        for service in services
    }

    return render_template(
        "dashboard.html",
        services=services,
        availability=availability,
        slow_threshold_ms=current_app.config.get(
            "SLOW_RESPONSE_MS", 1500
        ),
    )


@main.post("/check-now")
def check_now():
    results = run_all_checks()

    flash(
        f"Completed {len(results)} health check(s).",
        "success",
    )

    return redirect(url_for("main.dashboard"))


@main.get("/history")
def history():
    results = get_recent_results(limit=200)

    return render_template(
        "history.html",
        results=results,
    )
