#!/usr/bin/env bash
# Restore a backup into a NEW database (never overwrites an existing one).
# Usage: scripts/restore.sh <file.dump> <file_filestore.tar.gz> <new_db_name>
# Afterwards set DB_NAME=<new_db_name> in .env (and db_name/dbfilter in config/odoo.conf for prod),
# then: docker compose up -d --force-recreate odoo
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; source .env; set +a

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <file.dump> <file_filestore.tar.gz> <new_db_name>" >&2; exit 1
fi
DUMP="$1"; FILESTORE="$2"; NEWDB="$3"
[[ -f "$DUMP" && -f "$FILESTORE" ]] || { echo "Backup file not found." >&2; exit 1; }
[[ "$NEWDB" =~ ^[A-Za-z0-9_]+$ ]] || { echo "Database name: letters, digits, underscore only." >&2; exit 1; }

if docker compose exec -T db psql -U "$POSTGRES_USER" -d postgres -Atc \
     "SELECT 1 FROM pg_database WHERE datname='${NEWDB}'" | grep -q 1; then
  echo "Database '${NEWDB}' already exists. Choose a new name; this script never overwrites." >&2
  exit 1
fi

echo "Creating database ${NEWDB}..."
docker compose exec -T db createdb -U "$POSTGRES_USER" "$NEWDB"
echo "Restoring database..."
docker compose exec -T db pg_restore -U "$POSTGRES_USER" -d "$NEWDB" --no-owner < "$DUMP"
echo "Restoring filestore..."
docker compose exec -T odoo sh -c "mkdir -p /var/lib/odoo/filestore/${NEWDB} && tar -xzf - -C /var/lib/odoo/filestore/${NEWDB} --strip-components=1" < "$FILESTORE"
echo "Restored into '${NEWDB}'. Point DB_NAME at it and recreate the odoo container."
