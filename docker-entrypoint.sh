#!/bin/bash
set -e

function check_db_connection() {
  echo "Testing DB connection..."
  
  if ! nc -z db 5432; then
    echo "ERROR: Cannot reach PostgreSQL at db:5432"
    return 1
  fi

  if ! PGPASSWORD=$DB_PASS psql -h db -U $DB_USER -d $DB_NAME -c '\q'; then
    echo "ERROR: Failed to connect to PostgreSQL with provided credentials"
    echo "DB_HOST: $DB_HOST"
    echo "DB_USER: $DB_USER"
    echo "DB_NAME: $DB_NAME"
    return 1
  fi

  return 0
}

function init_db() {
  local retries=10
  local delay=2

  echo "Waiting for PostgreSQL to be ready..."

  until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' >/dev/null 2>&1 || [ $retries -eq 0 ]; do
    echo "Attempt $((11-retries)): PostgreSQL not ready, waiting..."
    sleep $delay
    ((retries--))
  done

  if [ $retries -eq 0 ]; then
    echo "ERROR: Failed to connect to PostgreSQL after 10 attempts"
    echo "Trying to connect with:"
    echo "host: $DB_HOST"
    echo "user: $DB_USER"
    echo "dbname: $DB_NAME"
    psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'
    exit 1
  fi

  echo "PostgreSQL is ready! Applying migrations..."
  alembic upgrade head

  echo "Initializing algorithm data..."
  PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    INSERT INTO algorithm (algorithm_id, name, type, description, is_symmetric) VALUES
    (1, 'AES-256', 'AES', 'Advanced Encryption Standard', true),
    (2, 'RSA-2048', 'RSA', 'Rivest-Shamir-Adleman', false),
    (3, 'ECC-P256', 'ECC', 'Elliptic Curve Cryptography', false)
    ON CONFLICT (algorithm_id) DO NOTHING;
EOSQL
}

init_db &

exec "$@"