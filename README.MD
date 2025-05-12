
This **Currency Conversion Microservice** is a FastAPI-based API that fetches live exchange rates from an external service, caches them in Redis for improved performance, and logs application activity with a dual-handler setup (file and console). It includes Pydantic-backed configuration, robust error handling, pytest-based tests with mocked external calls, and Docker support for ease of deployment.

---

## Project Overview

A small, maintainable FastAPI microservice that:

* Converts currency amounts via a third-party API.
* Caches exchange rates in Redis to minimize external calls.
* Provides structured logging: **DEBUG** logs to file and **WARNING+** logs to console. 

---

## Features

* **Stateless Processes**: Runs under Uvicorn, binding to a configurable port. 
* **Config via Env Vars**: Uses Pydantic’s `BaseSettings` for type-safe settings loaded from a `.env`. 
* **Redis Caching**: Stores rates with TTL to reduce latency and API usage.
* **Structured Logging**: Dual handlers—file (`DEBUG+`) and console (`WARNING+`).
* **Automated Tests**: pytest suite with HTTPX TestClient `requests`.
* **Containerized**: Dockerfile + docker-compose for local development (FastAPI + Redis).

---

## Requirements

* Python 3.13+
* Redis Server Redis 5.0.14+
* Docker & Docker Compose
* Environment variables defined in a `.env` file

---

## Installation

```bash
# Clone repository
git clone https://github.com/Prasun-Shiwakoti/currency-converter.git
cd currency-converter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` in the project root:

```dotenv
APP_NAME=Currency Converter API
EXCHANGE_RATE_API_KEY=28b17f9aedef73e0d9f7a6242102377a
EXCHANGE_RATE_API_URL=https://api.exchangerate.host/convert
REDIS_HOST_URL=localhost
REDIS_HOST_PORT=6379
```

* Pydantic’s `BaseSettings` loads these vars and validates types.
* Keep `.env` out of version control (`.gitignore`).

---

## Usage

```bash
# Run with Uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT

# Convert example
curl "http://localhost:8000/convert?from_currency=USD&to_currency=EUR&amount=100"
```

Response:

```json
{
  "from": "USD",
  "to": "EUR",
  "amount": 100,
  "exchange_rate": 0.898969,
  "converted_amount": 89.8969
}
```

---

## Caching with Redis

* Upon first request for a pair (e.g., `USD_EUR`), the rate is fetched and cached with `redis_client.setex(...)` for 1 hour. 
* Subsequent requests within TTL hit Redis, bypassing external API.
* Connection failures fall back gracefully, logging warnings.

---

## Testing

Install test requirements and run pytest:

```bash
pytest
```

* FastAPI’s TestClient is based on HTTPX. 
---

