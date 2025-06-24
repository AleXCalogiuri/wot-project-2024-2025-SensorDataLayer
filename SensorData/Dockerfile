# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

# Copio requirements
COPY requirements.txt requirements.txt

# Installo compilatori e dipendenze di build necessarie
RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Imposto variabili ambiente Flask
ENV PYTHONPATH=/app
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Copio tutto il progetto nel container
COPY . .

# Espongo la porta
EXPOSE 5000

# Comando di avvio
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
