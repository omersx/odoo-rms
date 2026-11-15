# odoo-rms — Retail Management System for Odoo 19 Community

A thin, opinionated retail layer on top of **native Odoo 19 Community**: two roles, a clean app
launcher, server-side guards for refunds and stock moves, and POS screens that survive a busy counter.

Not a fork of Odoo. Not a new POS, stock or accounting engine. One small add-on
(`custom_addons/retail_management`, 34 files, 22 automated tests) and **no changes to Odoo core**.

## What it adds over stock Odoo

| # | Feature | Where it lives |
|---|---|---|
| 1 | **Two roles** — Retail Cashier, Retail Manager — mapped onto native Odoo permission groups | `security/retail_security.xml` |
| 2 | **Refunds are manager-only**, enforced on the server (order and negative-quantity lines, so POS sync and RPC are covered) | `models/pos_order.py` |
| 3 | **Stock receipts/moves are manager-only** | `models/stock_picking.py` |
| 4 | One **Retail Management** app with the shop's screens — POS, products, inventory, invoicing, customers, settings — instead of Odoo's full app tree | `views/retail_menu.xml` |
| 5 | Full-page **icon launcher** (search + tiles), opened from the navbar Apps button; it re-reads the menus on open, so a menu you hide server-side stops showing a tile | `static/src/apps_page/` |
| 6 | **Installable as an app** (PWA): own icon and name, opens full screen | `static/description/icon.svg` |
| 7 | POS **payment screen**: methods in two columns, full-size icons, due total clamped for long amounts | `static/src/pos/payment_methods.scss` |
| 8 | **Receipt prints the QR only** — no portal URL, no short code | `static/src/pos/receipt.scss` |
| 9 | Payment icons stored at 256 px instead of Odoo's 50 px cap | `models/pos_payment_method.py` |
| 10 | **Camera Scan button + beep** on the product form's Barcode field | `static/src/fields/barcode_scan_field.*` |
| 11 | **Cashier workspace**: a two-tile app list (the shop app + Dashboards), Arabic labels, and a **read-only on-hand stock** screen (no new rights: quants are readable by any internal user, writable by nobody but stock users) | `security/retail_security.xml`, `data/hide_apps.xml`, `i18n/ar_001.po`, `views/stock_quant_readonly.xml` |
| 12 | Invoice **طرق الدفع** block built from the company's bank accounts, an `اسم العميل` heading, and `باستخدام <wallet>` on a paid invoice | `views/report_invoice.xml`, `views/company_bank_accounts.xml` |
| 13 | Invoice PDF **fits one A4 page**, is rendered in the **customer's language**, and is stored at posting — so the portal shows the real invoice, never a proforma | `models/account_move.py` |

## What it deliberately does not do

- No custom order, product, stock, invoice or payment models — those are Odoo's.
- No custom POS, no offline sync, no accounting or reporting engine.
- No core overrides; everything is a small inheritance or an asset addition.
- Hidden menus (Discuss, Contacts) are cosmetic; the security is in groups and server checks.

## Requirements

- **Odoo 19.0 Community** (verified on build `19.0-20261015`)
- PostgreSQL 16
- Docker + Docker Compose (the dev/prod kit is included), or any existing Odoo you can copy the add-on into

## Quick start (development)

```bash
git clone https://github.com/<your-account>/odoo-rms.git ~/rms && cd ~/rms
scripts/bootstrap.sh dev        # preflight, .env + config with random secrets, DB, Odoo up
docker compose run --rm odoo odoo -d rms -i retail_management --stop-after-init
docker compose restart odoo
```

Then open `http://localhost:8069` and change the admin password — a database created from the
command line starts with a default one.

## Customize it for your company (it is a template)

Nothing in the add-on hardcodes a shop. Everything below is **database data**, entered once per company:

| What | Where |
|---|---|
| Company name, address, logo, document footer | *Settings → Companies* |
| **Wallets shown as طرق الدفع on invoices**, plus the two wordings | *Settings → Companies → Invoices* page: bank accounts (`rms_payment_title`, `rms_payment_note`) |
| Products, prices, barcodes, stock | *Retail Management → Products* (write access needs *Retail Manager*) |
| Tax rates and "prices include tax" | *Invoicing → Configuration → Taxes* and *Settings → Taxes* |
| Register, payment methods, receipt footer | *Retail Management → Settings* (POS configuration) |
| Users | *Settings → Users*: give a cashier *Retail Cashier*, a manager *Retail Manager*; never *Settings*/*Administrator* |
| Language | each user's *Preferences* (Arabic `ar_001` ships with Odoo) |

No wallet number, account holder, product or price from a real shop is in this repository — those live in
the database and are yours to fill (D-045).

## Add to an existing Odoo

Copy `custom_addons/retail_management` into an add-ons path, add that path to `addons_path`, then:

```bash
odoo -d <db> -i retail_management --stop-after-init     # first install
odoo -d <db> -u retail_management --stop-after-init     # upgrade
```

## Tests

```bash
# install on a disposable database first
docker compose run --rm odoo odoo -d rms_test -i retail_management --stop-after-init
# then run this module's tests (with -u, only the updated module's tests run)
docker compose run --rm odoo odoo -d rms_test -u retail_management --test-enable --stop-after-init
```

Do not add `--test-enable` to the `-i` line: on a fresh database Odoo then runs the tests of *every*
installed module, including core ones that need a full build environment.

They cover the access rules (cashier vs manager): refunds, negative lines, stock validation, product and
quant writes, the menu/app list, plus invoice PDF rendering. Use a disposable database — the test run
creates and deletes POS orders.

## Repository layout

```
custom_addons/retail_management/   the add-on (models, views, security, assets, tests)
docker-compose.yml                 base compose file
docker-compose.dev.yml             dev overlay (localhost only)
docker-compose.prod.yml            prod overlay (Caddy + HTTPS, Odoo not published)
config/                            Odoo config templates (real config is git-ignored)
scripts/                           preflight, bootstrap, setup, backup, restore
deployment/                        Caddyfile
docs/                              spec, architecture, roadmap, decisions, deployment, agent workflow
```

## Customizing for another industry

Keep **one base module** and add thin per-industry modules that depend on it — never fork the repo
per customer. Most industry differences are configuration, not code. See
[`docs/INDUSTRY_VARIANTS.md`](docs/INDUSTRY_VARIANTS.md).

## Deployment

`docs/DEPLOYMENT.md` covers a hosted server and an always-on local store machine, both with HTTPS via
Caddy, plus backup/restore and an update procedure.

## Documentation

`docs/RETAIL_MANAGEMENT_SPEC.md` (scope) · `docs/ARCHITECTURE.md` (verified technical facts) ·
`docs/DEVELOPMENT_ROADMAP.md` (phases) · `docs/DECISIONS.md` (every non-trivial decision, with
alternatives) · `docs/PROJECT_STATE.md` (live maintainer state).

The project was built with an AI agent, and the working rules are part of the repo: `AGENTS.md`
(autonomy, hard stops, invariants), `docs/AGENT_PLAYBOOK.md` (debug/decide/escalate),
`docs/HANDOFF_PROMPT.md` (hand-over prompt). Adapt or delete them if you work differently.

## License

LGPL-3 — see [LICENSE](LICENSE). Odoo Community itself is LGPL-3 by Odoo S.A.

Copyright (C) 2026 odoo-rms contributors.

## Project status

Working and tested on Odoo 19.0 Community, verified on a clean install with no demo data. The retail core
(roles, guards, POS screens, launcher), the cashier workspace (customers, invoicing at the till and in the
back office, read-only stock) and the printable documents (receipt QR, one-page invoice with the payment
block) are in place; reports and a customer dashboard come next. The `docs/` folder is the live working
memory of the project, so it contains the maintainers' roadmap, decision log and current state rather than
polished user documentation. Nothing here has been used in production yet — try it on a disposable database
first, change the default passwords, and enter your own company, products, wallets and tax figures.
