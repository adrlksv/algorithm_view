set -e

function init_db() {
  local retries=10
  local delay=3

  echo "Attempting to connect to PostgreSQL..."

  until PGPASSWORD=$DB_PASS psql -h db -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null || [ $retries -eq 0 ]; do
    echo "Waiting for PostgreSQL to be ready, $((retries--)) remaining attempts..."
    sleep $delay
  done

  if [ $retries -eq 0 ]; then
    echo "Failed to connect to PostgreSQL after 10 attempts, exiting..."
    exit 1
  fi

  echo "PostgreSQL is ready, proceeding with migrations and initialization..."

  alembic upgrade head

  PGPASSWORD=$DB_PASS psql -h db -U $DB_USER -d $DB_NAME <<-EOSQL
    INSERT INTO algorithm (algorithm_id, name, type, description, is_symmetric) VALUES
    (1, 'AES-256', 'AES', 'Advanced Encryption Standard', true),
    (2, 'RSA-2048', 'RSA', 'Rivest-Shamir-Adleman', false),
    (3, 'ECC-P256', 'ECC', 'Elliptic Curve Cryptography', false)
    ON CONFLICT (algorithm_id) DO NOTHING;
EOSQL

  echo "Database initialization completed successfully"
}

init_db &

exec "$@"