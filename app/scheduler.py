
from apscheduler.schedulers.background import BackgroundScheduler

from config import CHECK_INTERVAL_SECONDS

_scheduler = None


# to start a scheduler to run API health checks at regular intervals (60 seconds, from config file)
# executes run_all_checks(), prevents duplicate scheduler instances
# runs checks based on CHECK_INTERVAL_SECONDS (60 seconds)

def start_scheduler(app):

    global _scheduler

    if _scheduler is not None and _scheduler.running:
        return _scheduler

    scheduler = BackgroundScheduler(daemon=True)

    def scheduled_job():
        with app.app_context():
            from app.monitor import run_all_checks
            run_all_checks()

    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        seconds=CHECK_INTERVAL_SECONDS,
        id="periodic-health-checks",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()
    _scheduler = scheduler

    return scheduler
