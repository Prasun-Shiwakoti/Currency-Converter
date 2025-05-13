from fastapi import FastAPI, HTTPException, Depends, Request
import requests
import logging
import redis

from app.config import get_settings
from app.logging_config import setup_logging

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


setup_logging()
logger = logging.getLogger("currency_converter")

settings = get_settings()

# Setting up redis to cache exchange rates
try:
    redis_client = redis.Redis(
        host=settings.redis_host_url, port=settings.redis_host_port, db=0
    )
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except redis.ConnectionError as e:
    logger.error(f"Redis connection failed: {e}")
    redis_client = None


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/convert")
def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: float,
    settings: dict = Depends(get_settings),
):
    # Logging request details
    logger.debug(f"Received request: {amount} {from_currency} to {to_currency}")

    cache_key = f"{from_currency}_{to_currency}"

    if redis_client:
        try:
            cached_rate = redis_client.get(cache_key)
        except Exception as e:
            logger.error(f"Redis error: {e}")
            cached_rate = None
    else:
        cached_rate = None

    if cached_rate:
        rate = float(cached_rate)
        logger.info(f"Cache hit for {cache_key}: {rate}")
        exchange_rate = rate
        converted_amount = amount * rate

    else:
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "access_key": settings.exchange_rate_api_key,
        }

        try:
            logger.info(
                f"Fetching exchange rate from external API for {from_currency} to {to_currency}"
            )
            response = requests.get(settings.exchange_rate_api_url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"External API error: {e}")
            raise HTTPException(status_code=500, detail="External API error") from e

        data = response.json()

        if not data.get("success", False):
            logger.warning(
                f"Invalid currency code or amount: {from_currency}, {to_currency}, {amount}"
            )
            raise HTTPException(
                status_code=400, detail="Invalid currency code or amount"
            )

        result = data.get("result")
        logger.info(f"Conversion result: {result}")

        exchange_rate = data.get("info").get("quote")
        converted_amount = amount * exchange_rate

        if redis_client:
            try:
                redis_client.setex(cache_key, 3600, exchange_rate)

                cache_key_inv = f"{to_currency}_{from_currency}"
                redis_client.setex(cache_key_inv, 3600, round(1 / exchange_rate, 4))
            except Exception as e:
                logger.error(f"Redis error: {e}")

    return {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
        "exchange_rate": exchange_rate,
        "converted_amount": converted_amount,
    }
