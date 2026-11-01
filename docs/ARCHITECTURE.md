# RMS Architecture

**Platform:** Odoo 19 Community Edition
**Status:** Baseline. Sections marked **TO VERIFY** are empty until the agent confirms them against the
real environment (Phase 0). Do not treat any unchecked statement as fact.

Product requirements live in `RETAIL_MANAGEMENT_SPEC.md`; progress lives in `DEVELOPMENT_ROADMAP.md`.

## 1. Principles
- Extend Odoo through custom add-ons only; never modify core.
- Reuse native POS, Stock, Invoicing/Accounting and Contacts.
- Keep custom code small and modular; prefer standard views/actions over custom frontend code.
- Enforce security on the server; preserve transaction and stock traceability.
- Verify every dependency and API against the exact Odoo 19 source.

## 2. Environment — VERIFIED for the dev stack (2026-11-01)

The dev stack runs. Evidence: `scripts/preflight.sh` 0 failures; `http://localhost:8069/web/login`
returns HTTP 200; versions read from inside the containers.

| Item | Value |
|---|---|
| Host OS | Windows 10 22H2 (10.0.19045) with WSL2 Ubuntu 24.04.2 LTS, kernel 6.18.54.1 |
| **Runtime option chosen** | ☑ Docker Desktop (confirmed working) ☐ WSL2 + Ubuntu native Odoo |
| Project location (must be Linux filesystem, not `/mnt/c`) | `/home/omer/rms` (`~/rms`); Windows copy kept as backup |
| Docker only: compose file path, Odoo image tag/digest, PostgreSQL image tag, volumes | `docker-compose.yml` + `docker-compose.dev.yml`; Odoo `mirror.gcr.io/library/odoo:19.0` @ `sha256:27f920e002c43a1af7022a68f3cc17db71a2f9f3348800cb050721ce54893e49`; PostgreSQL `mirror.gcr.io/library/postgres:16` @ `sha256:5db6dac2ef5dcff512f4f00a009c3c332b9f2f28f24277175bf3e4a3d02ef83a`; volumes `db-data`, `odoo-data` |
| Docker client / daemon | CLI 29.8.0, Compose 5.5.1; engine 29.8.0 reachable from Ubuntu via Docker Desktop WSL integration (enabled 2026-11-01) |
| WSL2 only: Odoo checkout path, virtualenv path | Not applicable (no native install) |
| Odoo version and source revision (commit/build) | `Odoo Server 19.0-20261015` (official image build 2026-10-15; no git revision exposed by the image) |
| Odoo source path | `/usr/lib/python3/dist-packages/odoo` (read-only inspection) |
| PostgreSQL version | `PostgreSQL 16.15 (Debian 16.15-1.pgdg13+2)` |
| Python version | `Python 3.12.3` |
| `odoo.conf` path and addons paths | Container `/etc/odoo/odoo.conf` (mounted from `config/`); effective addons: `/usr/lib/python3/dist-packages/odoo/addons`, `/var/lib/odoo/addons/19.0`, `/usr/lib/python3/dist-packages/addons`, plus `/mnt/extra-addons`. `data_dir=/var/lib/odoo`, `list_db=True`, `workers=0` |
| Custom addons directory | `./custom_addons` → `/mnt/extra-addons`. Odoo skips an addons path that contains no module (`tools/config.py:_is_addons_path`), hence a warning while the directory is empty; a module makes it valid after restart |
| Disposable test database name | `rms_test` (not created yet; created in Phase 1) |
| Command to start Odoo | `docker compose up -d` — **verified**; `scripts/bootstrap.sh dev` — works after the image workaround below |
| Command to install/upgrade module | `docker compose run --rm odoo odoo -d <db> -i <module> --stop-after-init` (base init verified; module install in Phase 1); upgrade with `-u` |
| Command to run tests | `docker compose run --rm odoo odoo -d rms_test -i <module> --test-enable --stop-after-init` — **not executed yet** (no module until Phase 1) |
| OpenCode version and configured model | OpenCode 1.19.1; `opencode.jsonc` default model `anthropic/claude-opus-5`; this session ran `opencode/deepseek-v4.1-flash-free` |
| OpenCode tools actually present (agents/skills/MCP/plugins) | Plugins `superpowers`, `@dietrichgebert/ponytail`; user skill `planning-with-files`; MCP servers `govinfo`, `courtlistener`, `rea` (none Odoo-related, not RMS tools); `claude-mem` plugin disabled; no Odoo agents/commands installed |
| Git remote / branch convention | Local repo only, **no remote**; branch `main`; commits `phase-N: summary`, tags `phase-N-done` |

**Image workaround (region-specific):** Docker Hub's blob CDN (`production.cloudfront.docker.com`)
returns `403 — "The Amazon CloudFront distribution is configured to block access from your country."`
for every layer, while manifest/auth requests work. `.env` therefore points at `mirror.gcr.io`
(Google's Docker Hub mirror). Digests were compared with the official manifests via
`docker buildx imagetools inspect` and are identical, so the content is the same official image.
Without this, `scripts/bootstrap.sh dev` fails at `docker compose pull`. See `DECISIONS.md` D-001.

**Odoo 19 CLI note:** `--without-demo` is a boolean since 19.0. The old `--without-demo=all` is invalid
(Odoo warns and assumes `True`); `bootstrap.sh` and `DEPLOYMENT.md` were corrected.

Safety: all development runs on a disposable database. Production is never touched by the agent.

## 3. Logical architecture

```text
Administrator / Cashier
        |
Retail workspace (Odoo web client)
  ├─ Dashboard / navigation
  ├─ Native POS
  ├─ Products & inventory views
  ├─ Customers (simple retail CRM)
  ├─ Invoicing views
  └─ Reports
        |
Custom add-on: retail_management   (workspace, menus, security mapping, small config)
        |
Odoo standard apps: POS · Stock · Product · Contacts · Accounting/Invoicing
        |
PostgreSQL
```

Conceptual only. Exact module names and dependencies are recorded in §4 once verified.

## 4. Module strategy and verified dependencies

**Core add-on (proposed):** `retail_management`
- Provides the Retail Management menu/workspace, dashboard entry points, role/group mapping, and
  minimal retail configuration or presentation extensions.
- Does **not** reimplement products, stock, POS, invoices, payments or accounting.
- Add models only after a verified gap; add POS JS/OWL only for an approved requirement, following
  Odoo 19 patterns (not copied from older versions).

**Suggested layout** (create only the files actually needed):
```text
custom_addons/retail_management/
├── __init__.py
├── __manifest__.py
├── models/            # only if a verified gap exists
├── views/             # menus, actions, settings views
├── security/          # groups, ir.model.access.csv, record rules
├── data/
├── static/description/icon.png
└── tests/
```

**Possible later add-ons** (only with owner approval): `retail_management_purchase`,
`retail_management_profiles`, `retail_management_inventory_only`.

**Dependency verification checklist** (Phase 0 → record results here):
1. List standard modules present in this Community build.
2. Read their manifests and transitive dependencies.
3. Confirm the custom add-on can depend on what it needs without pulling unwanted apps.
4. Record the dependency graph below.
5. Test a clean install and an upgrade on a disposable database.

| Module | Present in build? | Manifest depends | Notes |
|---|---|---|---|
| `point_of_sale` | | | |
| `stock` | | | |
| `account` | | | |
| `contacts` | | | |
| `product` | | | |
| `barcodes` (or equivalent) | | | |
| POS-stock integration module(s) | | | |
| `purchase` (extension) | | | |

## 5. Data ownership
Standard records are the source of truth (see spec §8). Model names, relations and fields must be
verified in the installed source and recorded here.

### Customer data strategy (simple CRM)
- **Profile:** native partner record. **Tags/groups:** native partner categories unless a real gap is verified.
- **History:** query customer-linked POS orders and invoices; never copy them into a history table.
- **Notes:** use a native notes/activity capability if suitable; otherwise a minimal access-controlled
  extension, after reviewing the exact Odoo 19 model and UX.
- **Insights:** order count, total purchases, last purchase — computed from source records. Define and
  document treatment of refunds, cancelled orders, taxes and currency first. Do not store aggregates
  unless performance evidence requires it.
- **Outstanding balance:** derived from native receivables/invoices; sensitive; authorized users only.
- Cashiers may search/select customers; creation only if enabled, limited to approved fields.

## 6. Security architecture
Roles: Administrator, Cashier. Approach:
- Map roles to verified Odoo groups and POS employee/access mechanisms; record the mapping in §6.1.
- ACLs for any custom model; record rules only for genuine row-level needs.
- Protect sensitive operations server-side: stock adjustments, refunds, price overrides, invoice
  posting, configuration, customer financial data.
- Test direct RPC/ORM access as well as the UI. Individual identities; transaction attribution retained.

### 6.1 Group mapping — TO VERIFY
| Retail role | Odoo groups / POS access | Evidence |
|---|---|---|
| Administrator | | |
| Cashier | | |

Candidate groups to check (names are unverified guesses): POS user/manager, stock user/manager,
accounting/invoicing groups, contact-creation group, and the technical/settings group that
Administrator should *not* automatically receive.

## 7. POS architecture
Use native POS; customize only where configuration or supported extension points cannot meet a
requirement. Verify on the exact build: sessions, cashier/employee attribution, payment methods,
receipts, refunds, POS-to-stock timing, offline storage/sync, and supported frontend extension APIs.
Document offline limitations (spec §6). No separate POS engine.

## 8. Inventory architecture
Use standard workflows for stock overview, receipts, movements, counts/adjustments, and (later)
transfers, lots/serials and reordering rules. Single-store first. Negative-stock behaviour must be
decided and tested (STK-07).

## 9. Environments and deployment
- **Development:** local Odoo 19 + disposable database.
- **Staging:** production-like, with test/anonymized data.
- **Production:** secured deployment, backups, monitoring, controlled upgrades.

Two supported development runtimes on Windows (see `WINDOWS_SETUP.md`): **Docker Desktop** and
**WSL2 + Ubuntu native Odoo**. Choose one in Phase 0 and record it in §2. The custom add-on code,
tests and documentation are identical for both. Docker is a development/deployment convenience, not
a product dependency. Pin the validated Odoo image tag/digest or source commit so builds do not
change silently.

The repository includes a Docker kit used for **local development, a local store server, and a hosted
server** (`docker-compose.yml` + `.dev.yml`/`.prod.yml`, `deployment/Caddyfile`, `scripts/`); see
`DEPLOYMENT.md`. The kit is **unverified until run** — record the result of the first real run here.

Production checklist: confirm Odoo build/revision and PostgreSQL compatibility; configure `addons_path`;
install verified dependencies and the custom add-on; configure company, currency, taxes, warehouse,
POS, journals, users; HTTPS and restricted access; backups with a tested restore; test printers and
scanners on target hardware; documented upgrade and rollback; no secrets or production data in Git.

## 10. Decisions to validate
| Decision | Direction | Status | Evidence / date |
|---|---|---|---|
| POS engine | Native Odoo POS | Unverified | |
| Inventory source | Native Stock | Unverified | |
| Invoice source | Native accounting | Unverified | |
| Custom code | Isolated add-ons | Unverified | |
| Administrator ≠ technical superuser | Separate where possible | Unverified | |
| Offline | Native POS only | Unverified | |
| Deployment kit (Compose + Caddy) | Same kit for dev, local server, hosted server | Syntax-checked only; not yet run | |
| Dev runtime | Docker Desktop **or** WSL2 native (owner chooses; Docker Desktop recommended if already installed) | Undecided | |
| Inventory-only profile | Future option | Unverified | |
| Purchasing | Extension | Unverified | |

## 11. Decision log
All decisions are recorded in `DECISIONS.md` (with tiers, alternatives and evidence). Summarize only
verified, lasting architecture facts here and reference the decision ID.

## 12. Known risks and open questions
(Agent maintains this list; remove items when resolved.)
