#!/usr/bin/env bash
# One-command DEVELOPMENT bootstrap: preflight -> .env/odoo.conf -> images -> database -> Odoo up.
# Safe to re-run: it never overwrites existing config, never drops data, never recreates an existing DB.
# Production is deliberately NOT supported here (see docs/DEPLOYMENT.md; needs a human).
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-dev}" != "dev" ]]; then
  echo "bootstrap.sh only supports 'dev'. Production deployment is a manual, approved step (docs/DEPLOYMENT.md)." >&2
  exit 1
fi

echo "== 1/6 Preflight =="
scripts/preflight.sh || { echo "Fix the FAIL items above, then re-run scripts/bootstrap.sh" >&2; exit 1; }

echo "== 2/6 Configuration =="
if [[ -e .env && -e config/odoo.conf ]]; then
  echo "Existing .env and config/odoo.conf kept."
elif [[ ! -e .env && ! -e config/odoo.conf ]]; then
  scripts/setup.sh dev
else
  echo "Only one of .env / config/odoo.conf exists. Resolve this manually (do not guess); see scripts/setup.sh." >&2
  exit 1
fi
set -a; source .env; set +a
case "${COMPOSE_FILE:-}" in
  *dev.yml*) ;; *) echo "COMPOSE_FILE in .env is not the dev stack ('${COMPOSE_FILE:-}'). Refusing." >&2; exit 1 ;;
esac

echo "== 3/6 Images =="
docker compose pull

echo "== 4/6 Database server =="
docker compose up -d db
for i in $(seq 1 30); do
  docker compose exec -T db pg_isready -U "$POSTGRES_USER" -d postgres >/dev/null 2>&1 && break
  sleep 2
  [[ $i -eq 30 ]] && { echo "PostgreSQL did not become ready." >&2; docker compose logs --tail 30 db >&2; exit 1; }
done
echo "PostgreSQL ready."

echo "== 5/6 Odoo database '${DB_NAME}' =="
EXISTS=$(docker compose exec -T db psql -U "$POSTGRES_USER" -d postgres -Atc \
         "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" || true)
if [[ "$EXISTS" == "1" ]]; then
  echo "Database ${DB_NAME} already exists. Leaving it untouched."
else
  docker compose run --rm odoo odoo -d "$DB_NAME" -i base --without-demo --stop-after-init
fi

echo "== 6/6 Start Odoo =="
docker compose up -d odoo
echo -n "Waiting for http://localhost:${ODOO_PORT:-8069} "
for i in $(seq 1 90); do
  code=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:${ODOO_PORT:-8069}/web/login" || true)
  if [[ "$code" == "200" || "$code" == "303" ]]; then echo " ready (HTTP $code)."; READY=1; break; fi
  echo -n "."; sleep 2
done
[[ "${READY:-0}" == "1" ]] || { echo; echo "Odoo did not respond in time. Recent logs:" >&2; docker compose logs --tail 40 odoo >&2; exit 1; }

echo
echo "== ENVIRONMENT FACTS (record these in docs/ARCHITECTURE.md section 2) =="
echo "Docker:   $(docker --version)"
echo "Compose:  $(docker compose version --short)"
echo "Odoo:     $(docker compose exec -T odoo odoo --version 2>/dev/null || echo 'not detected')"
echo "Postgres: $(docker compose exec -T db postgres --version 2>/dev/null || echo 'not detected')"
echo "Images:"; docker compose images 2>/dev/null || true
echo
echo "Odoo is at http://localhost:${ODOO_PORT:-8069} (database: ${DB_NAME})."
echo "IMPORTANT: a database created from the command line starts with login 'admin' and a default"
echo "password. Change the admin password in Odoo before doing anything else. Dev mode is reachable"
echo "from this computer only; never expose this database to a network unchanged."
