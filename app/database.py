import sqlite3
from datetime import datetime, timezone
from flask import current_app, g

# SQLite database connection and tables for services and API check results
# makes the database with sample services, gets service details and recent check results, and saves results
# calculates service availability percentage and closes the database connection when the Flask application ends

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_PATH"]
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            expected_status INTEGER NOT NULL DEFAULT 200,
            timeout_seconds REAL NOT NULL DEFAULT 5,
            enabled INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS check_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            checked_at TEXT NOT NULL,
            status TEXT NOT NULL,
            status_code INTEGER,
            response_time_ms REAL,
            error_message TEXT,
            FOREIGN KEY(service_id)
                REFERENCES services(id) ON DELETE CASCADE
        );
        """
    )

    count = db.execute(
        "SELECT COUNT(*) FROM services"
    ).fetchone()[0]
    if count == 0:
        now = datetime.now(timezone.utc).isoformat()

        examples = [
            (
                "HTTPBin OK demo",
                "https://httpbin.org/status/200",
                200, 5.0, 1, now,
            ),
            (
                "HTTPBin server-error demo",
                "https://httpbin.org/status/500",
                200, 5.0, 1, now,
            ),
        ]

        db.executemany(
            """
            INSERT INTO services
            (name, url, expected_status, timeout_seconds,
             enabled, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            examples,
        )

    db.commit()

def get_services_with_latest_results():
    db = get_db()

    return db.execute(
        """
        SELECT s.*,
               r.checked_at AS last_checked_at,
               r.status AS last_status,
               r.status_code AS last_status_code,
               r.response_time_ms AS last_response_time_ms,
               r.error_message AS last_error
        FROM services AS s
        LEFT JOIN check_results AS r
          ON r.id = (
              SELECT MAX(r2.id)
              FROM check_results AS r2
              WHERE r2.service_id = s.id
          )
        ORDER BY s.id
        """
    ).fetchall()

def save_check_result(service_id, result):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO check_results
        (service_id, checked_at, status, status_code,
         response_time_ms, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            service_id,
            result["checked_at"],
            result["status"],
            result["status_code"],
            result["response_time_ms"],
            result["error"],
        ),
    )

    db.commit()
    return cursor.lastrowid

def get_recent_results(limit=100):
    return get_db().execute(
        """
        SELECT r.*, s.name AS service_name,
               s.url AS service_url
        FROM check_results AS r
        JOIN services AS s ON s.id = r.service_id
        ORDER BY r.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

def get_availability(service_id, limit=100):

    rows = get_db().execute(
        """
        SELECT status FROM check_results
        WHERE service_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (service_id, limit),
    ).fetchall()

    if not rows:
        return None

    up_count = sum(
        1 for row in rows if row["status"] == "UP"
    )

    return round(up_count / len(rows) * 100, 2)

def register_close_db(app):
    app.teardown_appcontext(close_db)
