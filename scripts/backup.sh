#!/usr/bin/env bash
# Back up the Odoo database and filestore into $BACKUP_DIR (default ./backups).
# Both files are needed for a full restore. Old backups older than BACKUP_KEEP_DAYS are removed.
# Run from anywhere; requires the stack to be running.
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; source .env; set +a

DEST="${BACKUP_DIR:-./backups}"
KEEP="${BACKUP_KEEP_DAYS:-14}"
STAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEST"

echo "Dumping database ${DB_NAME}..."
docker compose exec -T db pg_dump -U "$POSTGRES_USER" -Fc "$DB_NAME" > "$DEST/${DB_NAME}_${STAMP}.dump"

echo "Archiving filestore..."
docker compose exec -T odoo tar -C /var/lib/odoo/filestore -czf - "$DB_NAME" > "$DEST/${DB_NAME}_${STAMP}_filestore.tar.gz"

find "$DEST" -type f -name "${DB_NAME}_*" -mtime +"$KEEP" -delete
echo "Done: $DEST/${DB_NAME}_${STAMP}.dump and ..._filestore.tar.gz"
echo "Copy these OFF this machine too, and test a restore regularly."
