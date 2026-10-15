
# API Health Monitor

Made by- Kavya Anil (anilkavya266@gmail.com)

A Python web-based API monitoring dashboard using Flask to track API health, HTTP status codes, response times, and availability, including check history using SQLite and automated testing with GitHub Actions

## Features

- HTTP health checks using Requests
- UP, DEGRADED, and DOWN status classification
- Configurable expected status codes and timeouts
- Response-time measurement
- SQLite storage for check history
- Background scheduled checks
- Flask dashboard and history page
- Automated tests with pytest
- GitHub Actions testing & continuous integration

## Tech Stack

Python, Flask, Requests, SQLite, APScheduler, pytest, GitHub Actions.

## Setup

Install python.

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


