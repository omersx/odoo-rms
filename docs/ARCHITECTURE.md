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

**Verification results (2026-11-01).** The image has **692 modules with a manifest**. It is
Community-only: `account_accountant`, `web_enterprise`, `helpdesk`, `sale_subscription` and `quality`
are absent (`mrp` is present and is Community). Manifests were read from
`/usr/lib/python3/dist-packages/odoo/addons/*/__manifest__.py` in the running container.

| Module | Present in build? | Manifest depends | Notes |
|---|---|---|---|
| `point_of_sale` | yes | `resource`, `stock_account`, `barcodes`, `html_editor`, `digest`, `phone_validation`, `partner_autocomplete`, `iot_base`, `google_address_autocomplete` | Pulls **Stock + Invoicing** through `stock_account` |
| `stock` | yes | `product`, `barcodes_gs1_nomenclature`, `digest` | |
| `account` | yes | `base_setup`, `onboarding`, `product`, `analytic`, `portal`, `digest` | "Invoicing"; full accounting UI needs `account.group_account_user` |
| `contacts` | yes | `base`, `mail` | **Not** pulled by `point_of_sale` |
| `product` | yes | `base`, `mail`, `uom` | |
| `barcodes` | yes | `web` | Required by `stock` and `point_of_sale` |
| POS–stock/account integration | yes | `stock_account` depends on `stock`, `account` | There is no separate `pos_stock`; integration lives in `point_of_sale` + `stock_account` |
| `pos_hr` | yes | `point_of_sale`, `hr` | Employee/cashier login and `employee_id` attribution |
| `pos_discount` | yes | `point_of_sale` | Optional discount button; no security file (no group restriction) |
| `purchase`, `purchase_stock` | yes | `account` / `stock_account`, `purchase` | Planned extension only; not an MVP dependency |
| `pos_restaurant`, `pos_sale`, `pos_self_order` | yes | `point_of_sale` … | Not needed for RMS |

**Verified dependency chain:** `point_of_sale → stock_account → stock + account`; `stock → product`;
`account → product`; `contacts` is independent. Installing `point_of_sale` therefore already installs
Product, Stock and Invoicing, but not Contacts, Purchase, `pos_hr` or `pos_discount`.

**Proposed custom add-on dependency:** `['point_of_sale', 'stock', 'account', 'contacts']` (the first
three document direct use of POS/stock/account models and views; they are already transitive). Add
`pos_hr` only if the owner chooses employee-PIN login, and `pos_discount` only if discounts are enabled.
Do **not** depend on `purchase` in Milestone A.

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

### 6.1 Group mapping — VERIFIED on `rms_test` (2026-11-01)

| Retail role | Odoo groups / POS access | Evidence |
|---|---|---|
| **Administrator** | `base.group_user` · `point_of_sale.group_pos_manager` · `stock.group_stock_manager` · `product.group_product_manager` · `account.group_account_invoice` · `base.group_partner_manager` — **not** `base.group_system` by default | Group XML IDs and ACLs read from `rms_test`; `product.template` write needs `product.group_product_manager`, `stock.quant` write needs `stock.group_stock_user/manager`, `res.partner` create needs `base.group_partner_manager` |
| **Cashier** | `base.group_user` · `point_of_sale.group_pos_user` only | Same source. Gives pos.order/payment CRUD, product/partner read, stock.move/picking write, account.move read; no product/stock/partner-manager/accounting groups |

Verified details and gaps (must be handled in Phase 2/4, not assumed solved):
- A POS user's role is **manager** if they have `point_of_sale.group_pos_manager` **or**
  `account.group_account_invoice` (`point_of_sale/models/res_users.py:26`). Never give a cashier
  accounting groups.
- `pos.order` and `pos.payment` ACLs give POS users **create/write/unlink**; `stock.move` and
  `stock.picking` give create/write/unlink. Cashiers therefore need explicit server-side guards for
  validated orders/refunds/stock changes; the ACL alone is not least privilege.
- `point_of_sale/security/point_of_sale_security.xml` only has **multi-company** rules for POS
  orders/sessions/configs — there is **no** "own orders only" rule. The spec's "cashier sees own
  orders only" needs a record rule (Tier 2 decision).
- `pos.config.restrict_price_control` ("Restrict Price Modifications to Managers") exists, but is
  enforced **client-side only** (`static/src/app/services/pos_store.js:1400`). Server-side enforcement
  is custom work if the spec requires it.
- `pos.order._refund()` (`models/pos_order.py:1426`) has **no group check**; native refund permission is
  not a POS-group restriction. Admin-only refunds require a custom server-side check.
- Cashier contact creation is **off** by default (`res.partner` create only via
  `base.group_partner_manager`). Native POS can still select existing customers for invoices.
- `pos_hr` employee login: `pos.config.minimal_employee_ids` / `basic_employee_ids` /
  `advanced_employee_ids`; POS orders get `employee_id` ("Cashier"); users with the POS manager role
  are auto-added to `advanced_employee_ids` (`pos_hr/models/pos_config.py`). This is the mechanism for
  per-cashier attribution and multi-cashier sessions.
- `base.group_system` is Odoo's technical settings/administrator group. Whether day-to-day retail admin
  can work without it must be tested in Phase 2 (menus/actions may require it). UI hiding is not security.

## 7. POS architecture (verified source, 2026-11-01)

Native POS only. Confirmed on this build:

- **App structure:** OWL app under `point_of_sale/static/src/app` — services (`app/services`),
  models (`app/models`), components/screens. Assets are declared in the `point_of_sale._assets_pos`
  bundle; extra assets go under `static/src` (manifest comment says no manual bundle entry needed
  except ordering-sensitive SCSS).
- **Extension points:** models register in `registry.category("pos_available_models")`; behaviour is
  extended with `patch()` from `@web/core/utils/patch` (e.g. `pos_hr` patches `PosOrder`,
  `DataServiceOptions`, `Navbar`, `Chrome`). Custom POS JS must follow this Odoo 19 pattern.
- **Sessions/cashiers:** native sessions; `pos_hr` adds employee login and `pos.order.employee_id`;
  session has `employee_id`; POS manager role is `point_of_sale.group_pos_manager` (see §6.1).
- **Payments:** configured via `pos.payment.method` (cash journal minimum); no custom payment engine.
- **Refunds:** `pos.order.refund()` → `_refund()` copies the order into the current session; no group
  check in the method (see §6.1). Original/refund links are native.
- **POS → stock/accounting:** handled by `point_of_sale` + `stock_account`; stock moves/pickings are
  created on validation. Do not write quants or bypass these flows.
- **Offline (native, limited):** browser data and state are stored in **IndexedDB**
  (`app/services/data_service.js`, `app/models/utils/indexed_db.js`). Paid orders are kept locally and
  tracked (`localUnsyncedPaidOrderUuids`) until confirmed synced; sync runs on reconnect. The navbar
  shows an offline indicator; **opening a register/session while offline is refused**; product reload
  is disabled offline; reloading while offline warns that unsaved data may be lost. There is no
  real-time stock or order sharing between terminals. Runtime acceptance tests are Phase 8; no claims
  beyond this source reading.

**Customization rule:** configuration first. Custom POS JS only for an approved requirement, using the
registries/`patch` above; custom restrictions on refunds/price/orders must be **server-side**.

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
`DEPLOYMENT.md`. The **dev mode** of the kit was run on 2026-11-01 and works (`http://localhost:8069`);
the prod modes (Caddy/TLS, backup/restore, hosted server) remain unverified until Phase 8.

Production checklist: confirm Odoo build/revision and PostgreSQL compatibility; configure `addons_path`;
install verified dependencies and the custom add-on; configure company, currency, taxes, warehouse,
POS, journals, users; HTTPS and restricted access; backups with a tested restore; test printers and
scanners on target hardware; documented upgrade and rollback; no secrets or production data in Git.

## 10. Decisions to validate
| Decision | Direction | Status | Evidence / date |
|---|---|---|---|
| POS engine | Native Odoo POS | Verified | Source + running image, 2026-11-01 |
| Inventory source | Native Stock | Verified | `stock` installed with POS via `stock_account` |
| Invoice source | Native accounting | Verified | `account` installed with POS via `stock_account` |
| Custom code | Isolated add-ons | Unverified | Tested in Phase 1 |
| Administrator ≠ technical superuser | Separate where possible | Unverified | Test in Phase 2 (settings menus may need `base.group_system`) |
| Offline | Native POS only | Verified on paper | IndexedDB + sync + offline guards, 2026-11-01; runtime test Phase 8 |
| Deployment kit (Compose + Caddy) | Same kit for dev, local server, hosted server | Dev verified; prod not run | 2026-11-01 dev stack |
| Dev runtime | Docker Desktop | Verified | WSL integration enabled 2026-11-01 |
| Inventory-only profile | Future option | Unverified | Needs dependency validation |
| Purchasing | Extension | Present, not used | `purchase` + `purchase_stock` in build |

## 11. Decision log
All decisions are recorded in `DECISIONS.md` (with tiers, alternatives and evidence). Summarize only
verified, lasting architecture facts here and reference the decision ID.

## 12. Known risks and open questions

1. **Cashier ACL breadth** (Phase 2): `point_of_sale.group_pos_user` allows full CRUD on `pos.order`
   and `pos.payment`, and create/write on `stock.move`/`stock.picking`, plus read on `account.move`.
   Needs server-side guards/record rules; do not assume the UI prevents it.
2. **No own-orders record rule** for POS: cashiers can read all POS orders of the company by default.
   A rule is required for the spec's "own orders only" (Tier 2).
3. **Refunds and price overrides** have no server-side group check (`_refund()`; client-side
   `restrict_price_control`). Custom checks are required for admin-only approval.
4. **Docker Hub geo-block** (D-001): dev images come from `mirror.gcr.io`. Production deployment in this
   country needs a VPN/proxy or an approved mirror; plan this before Phase 8.
5. **WSL memory**: 3 GB visible; installs/tests are slow and may hit memory limits. 8 GB recommended.
6. **Community scope**: no Enterprise modules (`account_accountant`, `web_enterprise`, etc.). Confirm
   that the required invoicing/reporting features exist in Community before Milestone B.
7. **Empty `custom_addons/`**: Odoo skips the addons path until it contains a module (expected; Phase 1).
