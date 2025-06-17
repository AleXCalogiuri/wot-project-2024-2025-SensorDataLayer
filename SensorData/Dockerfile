# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV FLASK_APP=app.app.py
ENV FLASK_RUN_HOST=0.0.0.0
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
COPY . .
EXPOSE 5000
CMD ["flask", "run", "--host","0.0.0.0"]