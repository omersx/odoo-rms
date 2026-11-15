#!/usr/bin/env bash
# Create .env and config/odoo.conf with freshly generated secrets.
# Usage:  scripts/setup.sh dev
#         scripts/setup.sh prod [domain]      e.g. scripts/setup.sh prod shop.example.com
# Never overwrites existing files.
set -euo pipefail
cd "$(dirname "$0")/.."

MODE="${1:-}"
DOMAIN="${2:-localhost}"
if [[ "$MODE" != "dev" && "$MODE" != "prod" ]]; then
  echo "Usage: scripts/setup.sh dev|prod [domain]" >&2; exit 1
fi
if [[ -e .env || -e config/odoo.conf ]]; then
  echo "Refusing to overwrite existing .env or config/odoo.conf." >&2
  echo "Delete them yourself (after saving any passwords) if you really want new ones." >&2
  exit 1
fi
command -v openssl >/dev/null || { echo "openssl is required." >&2; exit 1; }

rand() { openssl rand -base64 36 | tr -d '/+=\n' | cut -c1-28; }
PG_PASSWORD="$(rand)"
ADMIN_PASSWD="$(rand)"
DB_NAME="rms"

if [[ "$MODE" == "dev" ]]; then
  COMPOSE_FILE_VALUE="docker-compose.yml:docker-compose.dev.yml"
else
  COMPOSE_FILE_VALUE="docker-compose.yml:docker-compose.prod.yml"
fi

sed -e "s|__COMPOSE_FILE__|${COMPOSE_FILE_VALUE}|" \
    -e "s|__PG_PASSWORD__|${PG_PASSWORD}|" \
    -e "s|__DOMAIN__|${DOMAIN}|" \
    .env.example > .env
sed -e "s|__ADMIN_PASSWD__|${ADMIN_PASSWD}|" \
    -e "s|__DB_NAME__|${DB_NAME}|g" \
    "config/odoo.conf.${MODE}.example" > config/odoo.conf
# .env is read only by Docker Compose on the host; odoo.conf must be readable by the container's
# 'odoo' user (a different uid), so it cannot be 600.
chmod 600 .env
chmod 644 config/odoo.conf

echo "Created .env and config/odoo.conf in '${MODE}' mode."
echo "Secrets are stored ONLY in those two files (ignored by Git). Save them in a password manager."
echo
echo "Next:"
echo "  1. Check image tags in .env (ODOO_IMAGE, POSTGRES_IMAGE)."
echo "  2. docker compose up -d db"
echo "  3. Create the database (see docs/DEPLOYMENT.md section 3), then: docker compose up -d"
