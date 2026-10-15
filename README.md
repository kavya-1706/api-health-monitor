
# API Health Monitor

Made by- Kavya Anil (anilkavya266@gmail.com)

A Python-based API monitoring tool that periodically checks HTTP endpoints, measures response times, stores check history in SQLite, and displays results on a Flask dashboard.

## Features

- HTTP health checks using Requests
- UP, DEGRADED, and DOWN status classification
- Configurable expected status codes and timeouts
- Response-time measurement
- SQLite storage for check history
- Background scheduled checks
- Flask dashboard and history page
- Automated tests with pytest
- GitHub Actions continuous integration

## Tech Stack

Python, Flask, Requests, SQLite, APScheduler, pytest, GitHub Actions.

## Setup

Make sure Python is installed, then open a terminal in the project folder.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python run.py
```

Open http://127.0.0.1:5000 in your browser.

## Run Tests

```bash
python -m pytest -q
```

## Health Rules

- UP: expected HTTP status and response time within threshold
- DEGRADED: unexpected HTTP status or slow response
- DOWN: timeout or request/network error

Availability is calculated from sampled check results. It is not a guarantee of continuous uptime.

