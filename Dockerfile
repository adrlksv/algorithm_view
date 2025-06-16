FROM node:18 AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM python:3.11.12-bullseye AS backend-builder

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

RUN apt-get update && apt-get install -y \
    iputils-ping \
    netcat \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .
COPY docker-entrypoint.sh .
COPY .env .env

ENV PYTHONPATH=/app

FROM python:3.11.12-bullseye

WORKDIR /app

COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

COPY --from=backend-builder /app /app

COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

COPY --from=backend-builder /app/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint.sh"]