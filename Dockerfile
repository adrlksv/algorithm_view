FROM python:3.11.12-bullseye as backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-dev gcc musl-dev postgresql-client

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . .

FROM node:18 as frontend

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./

RUN npm install

COPY frontend .

RUN npm run build

FROM python:3.11.12-bullseye

WORKDIR /app

COPY --from=backend /app /app

COPY --from=frontend /app/dist /app/frontend/dist

RUN apt-get update -y && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]