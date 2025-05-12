FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${APP_PORT}

CMD uvicorn app.main:app --host ${APP_HOST_URL} --port ${APP_PORT} --reload