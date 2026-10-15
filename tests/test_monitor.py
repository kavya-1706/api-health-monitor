
import requests

from app.monitor import check_api


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def test_expected_status_is_up(monkeypatch):
    monkeypatch.setattr(
        "app.monitor.requests.get",
        lambda *args, **kwargs: FakeResponse(200),
    )

    result = check_api("https://service.test", expected_status=200)

    assert result["status"] == "UP"
    assert result["status_code"] == 200
    assert result["error"] is None


def test_unexpected_status_is_degraded(monkeypatch):
    monkeypatch.setattr(
        "app.monitor.requests.get",
        lambda *args, **kwargs: FakeResponse(500),
    )

    result = check_api("https://service.test", expected_status=200)

    assert result["status"] == "DEGRADED"
    assert result["status_code"] == 500


def test_timeout_is_down(monkeypatch):
    def raise_timeout(*args, **kwargs):
        raise requests.exceptions.Timeout("timed out")

    monkeypatch.setattr(
        "app.monitor.requests.get", raise_timeout
    )

    result = check_api("https://service.test")

    assert result["status"] == "DOWN"
    assert result["status_code"] is None


def test_connection_error_is_down(monkeypatch):
    def raise_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError("unreachable")

    monkeypatch.setattr(
        "app.monitor.requests.get", raise_error
    )

    result = check_api("https://service.test")

    assert result["status"] == "DOWN"
    assert "ConnectionError" in result["error"]


def test_slow_response_is_degraded(monkeypatch):
    monkeypatch.setattr(
        "app.monitor.requests.get",
        lambda *args, **kwargs: FakeResponse(200),
    )

    ticks = iter([10.0, 12.0])

    monkeypatch.setattr(
        "app.monitor.time.perf_counter",
        lambda: next(ticks),
    )

    result = check_api(
        "https://service.test",
        slow_threshold_ms=100,
    )

    assert result["status"] == "DEGRADED"
    assert result["response_time_ms"] == 2000.0
