#!/usr/bin/env bash
# Read-only environment check. Installs and changes NOTHING.
# Exit code 0 = ready, 1 = something required is missing (see the FAIL lines).
cd "$(dirname "$0")/.." || exit 1
FAIL=0; WARN=0
ok()   { echo "  [ OK ] $*"; }
warn() { echo "  [WARN] $*"; WARN=$((WARN+1)); }
fail() { echo "  [FAIL] $*"; FAIL=$((FAIL+1)); }

echo "RMS preflight check"
echo "-------------------"

# Use the project's own port if .env already exists, so the port check below is about this stack.
if [ -f .env ]; then set -a; . ./.env; set +a; fi

# 1. Where are we running?
if grep -qi microsoft /proc/version 2>/dev/null; then ok "Running inside WSL"
else warn "Not inside WSL (fine on native Linux; on Windows run this from the Ubuntu/WSL terminal)"; fi

case "$(pwd -P)" in
  /mnt/*) fail "Project is under $(pwd -P). Move it to the Linux filesystem (e.g. ~/rms); /mnt/c is slow and breaks permissions." ;;
  *)      ok "Project path is in the Linux filesystem: $(pwd -P)" ;;
esac

# 2. Required commands
for c in git openssl curl; do
  command -v "$c" >/dev/null 2>&1 && ok "$c found" \
    || fail "$c missing. Install it (needs admin): sudo apt update && sudo apt install -y $c"
done

# 3. Docker
if ! command -v docker >/dev/null 2>&1; then
  fail "docker not found in this terminal. Install Docker Desktop and enable Settings > Resources > WSL integration for this Ubuntu distro."
else
  ok "docker CLI found ($(docker --version 2>/dev/null))"
  if docker info >/dev/null 2>&1; then ok "Docker daemon reachable"
  else fail "Docker daemon not reachable. Start Docker Desktop and enable WSL integration for this distro."; fi
  if docker compose version >/dev/null 2>&1; then ok "docker compose found ($(docker compose version --short 2>/dev/null))"
  else fail "docker compose (v2 plugin) not available."; fi
fi

# 4. Odoo port (dev mode)
PORT="${ODOO_PORT:-8069}"
if (exec 3<>/dev/tcp/127.0.0.1/"$PORT") 2>/dev/null; then
  warn "Port $PORT already answers. If it is not this project's Odoo, change ODOO_PORT in .env."
else ok "Port $PORT is free"; fi

# 5. Resources
FREE_GB=$(df -Pk . 2>/dev/null | awk 'NR==2{printf "%d", $4/1024/1024}')
if [ -n "$FREE_GB" ] && [ "$FREE_GB" -lt 10 ]; then warn "Only ${FREE_GB} GB free disk here (10+ GB recommended)."
else ok "Disk space: ${FREE_GB:-?} GB free"; fi
MEM_GB=$(awk '/MemTotal/{printf "%d", $2/1024/1024}' /proc/meminfo 2>/dev/null)
if [ -n "$MEM_GB" ] && [ "$MEM_GB" -lt 4 ]; then warn "WSL/host memory ${MEM_GB} GB (4+ GB recommended; raise it in %UserProfile%\\.wslconfig)."
else ok "Memory visible: ${MEM_GB:-?} GB"; fi

# 6. Project files
for f in docker-compose.yml docker-compose.dev.yml .env.example config/odoo.conf.dev.example scripts/setup.sh; do
  [ -e "$f" ] && ok "$f present" || fail "$f missing"
done

echo "-------------------"
echo "Result: ${FAIL} failure(s), ${WARN} warning(s)"
[ "$FAIL" -eq 0 ]
