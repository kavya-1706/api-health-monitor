
from app import create_app


def test_dashboard_loads(tmp_path):
    db_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "DATABASE_PATH": str(db_path),
    })

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Service dashboard" in response.data


def test_history_loads(tmp_path):
    db_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "DATABASE_PATH": str(db_path),
    })

    client = app.test_client()
    response = client.get("/history")

    assert response.status_code == 200
    assert b"Recent check history" in response.data
