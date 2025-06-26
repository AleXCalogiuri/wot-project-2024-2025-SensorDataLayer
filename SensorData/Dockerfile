# syntax=docker/dockerfile:1
FROM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# Crea la directory per il database
RUN mkdir -p /data
# Spostati nella directory SensorData
WORKDIR /app/SensorData

ENV PYTHONPATH=/app
ENV FLASK_APP=app.app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]