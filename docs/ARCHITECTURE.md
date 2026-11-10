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

**Core add-on (created 2026-11-01):** `retail_management`
- Provides the Retail Management menu/workspace, dashboard entry points, role/group mapping, and
  minimal retail configuration or presentation extensions.
- Does **not** reimplement products, stock, POS, invoices, payments or accounting.
- Add models only after a verified gap; add POS JS/OWL only for an approved requirement, following
  Odoo 19 patterns (not copied from older versions).

**Current content (2026-11-03):**

```text
custom_addons/retail_management/
├── __init__.py            # Python models added when a gap is verified
├── __manifest__.py        # depends: point_of_sale, stock, account, contacts
├── data/hide_apps.xml     # hides Discuss and Contacts from the app switcher — D-011, D-012
├── models/pos_order.py    # refund guard
├── models/stock_picking.py# receipt/move guard
├── security/retail_security.xml  # Retail Cashier / Retail Manager groups
├── static/description/icon.png   # app icon (drawn locally, no external asset)
├── static/src/apps_page/apps_page.js  # full-page app launcher client action — D-014
├── static/src/scss/apps_page.scss     # launcher styling — D-014
├── static/src/xml/apps_button.xml     # navbar button that opens the launcher — D-014
├── static/src/xml/apps_page.xml       # launcher template — D-014
├── tests/test_security.py
├── views/apps_page_action.xml  # ir.actions.client for the launcher — D-014
└── views/retail_menu.xml  # Retail Management menu → native actions
```

**App switcher (D-013 → D-014):** Odoo 19 replaced the full-page icon launcher with a plain text
dropdown (`web.NavBar.AppsMenu` renders `DropdownItem` with `t-esc="app.name"`; there is no `/odoo`
home-menu grid and the string "Search menus" does not exist in the `web` addon). The grid in the
owner's reference screenshots is Odoo 16–18 or a third-party backend theme. We restore it as a
**client action** (`retail_management.apps_page`): the navbar button is an inherited QWeb template that
calls `action.doAction`, and the page renders `app.webIconData` (already provided by the server from
each menu's `web_icon`) with a live search filter. No core file is touched and mobile keeps Odoo's own
sidebar. Verified in a browser: 7 tiles, search filter, tile navigation.
Note for future asset work: this build compiles SCSS with **libsass**, which rejects CSS `min()` with
mixed units and silently breaks the whole `web.assets_web` stylesheet.

**Workspace menus (verified on `rms_test2`)** — every item points at a native action, so no logic is
duplicated and native ACLs still apply:

| Menu | Native action | Groups on the item |
|---|---|---|
| Point of Sale | `point_of_sale.action_pos_config_kanban` (register list → Open) | `point_of_sale.group_pos_user,group_pos_manager` |
| Products | `stock.product_template_action_product` | none (native ACL: cashiers get read only) |
| Inventory | `stock.action_view_quants` (server action → quants) | `stock.group_stock_user` |
| Invoicing | `account.action_move_out_invoice` | `account.group_account_invoice` |
| Customers | `contacts.action_contacts` | `base.group_partner_manager` |
| Settings | `point_of_sale.action_pos_configuration` | `point_of_sale.group_pos_manager` |

Verified menu visibility (`ir.ui.menu._visible_menu_ids`): cashier (`group_pos_user`) sees **Point of
Sale + Products** (read-only); the mapped Administrator groups see **all but Settings**. Settings stays
hidden because `res.config.settings` needs `base.group_system` — this is the Phase 2 decision on
Administrator vs technical superuser (see §6.1 and risk 6).

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

**Custom add-on dependency:** `['point_of_sale', 'stock', 'account', 'contacts']` (the first three
document direct use of POS/stock/account models and views; they are already transitive). Owner
delegated the open choices (2026-11-01): no `pos_hr` (cashier identity = own Odoo user, which already
gives `pos.order.user_id`), no `pos_discount` (no discount button in Milestone A), no `purchase`.
See D-002 and D-003.

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

### 6.2 Retail roles as implemented (Phase 2, verified on `rms_test4`)

| Retail role | XML ID | Implied group IDs |
|---|---|---|
| **Retail Cashier** | `retail_management.group_retail_cashier` | `base.group_user`, `point_of_sale.group_pos_user` |
| **Retail Manager** | `retail_management.group_retail_manager` | `group_retail_cashier`, `point_of_sale.group_pos_manager`, `stock.group_stock_manager`, `product.group_product_manager`, `account.group_account_invoice`, `base.group_partner_manager` |

Deliberately absent: `base.group_system` (Odoo technical/settings superuser). Consequence: the Settings
menu and `res.config.settings` remain hidden from Retail Managers. Phase 2 follow-up recorded in risk 6.

**Server-side enforcement added** (`models/pos_order.py`):
- `pos.order._refund()` raises `AccessError` for non-managers — covers the backend "Return Products".
- `pos.order.line.create()/write()` raise `AccessError` when `qty < 0` for non-managers — this is the
  real enforcement point, because POS-frontend refunds are created client-side and pushed through
  `pos.order.create_from_ui` → `_process_order` → order/line creation. A negative quantity is the POS
  way to record a refund.

**Verified tests** (`tests/test_security.py`, 10 tests, run with
`-d rms_test4 -u retail_management --test-enable --test-tags /retail_management`):
cashier denied product creation, quant writes, contact creation, refund line, backend refund and
self-promotion to manager; cashier allowed to read products and to create normal (positive) sale lines;
manager allowed to refund and create products. Result: **0 failed, 0 errors**.

**Deferred to a decision (D-006):** the "cashier sees only own POS orders" record rule is **not**
implemented. A read rule on `pos.order` would filter `pos.session.order_ids` for non-sudo computations
(`pos_session.py` lines 246, 268, 391, 1736 use `order_ids` without `sudo`), so a cashier closing a
session would compute wrong totals and cash differences. Money correctness beats a cosmetic privacy
rule until a session-scoped rule is designed and tested in Phase 4.

**Known residual limitation (D-007):** `pos.config.restrict_price_control` ("Restrict Price
Modifications to Managers") is enforced **client-side only** (`pos_store.js:1400`). Price override by a
cashier is therefore not blocked server-side in Milestone A; enabling the config flag is the mitigation.
A server guard on `price_unit` is fragile (pricelists, taxes, rounding) and is deferred.

### 6.3 Permission matrix — reality check (Phase 2, 2026-11-01)

Status legend: **Enforced** = blocked/allowed at model level and covered by a test · **Config** = Odoo
setting, client-side or admin-gated by native ACL only · **Gap** = documented residual risk (decision
ID) · **B** = Milestone B.

| Function (spec §3) | Administrator | Cashier | Status |
|---|---|---|---|
| Use POS | yes | yes | Enforced (native POS user/manager ACLs) |
| Open/close POS session | yes | yes by default | Config — native POS allows a POS user to close a session; "configurable" is not implemented |
| View own POS orders | yes | yes | Enforced (native ACL) |
| View all POS orders | yes | **yes (gap)** | Gap — D-006, deferred to Phase 4 |
| Create/edit products | yes | no | Enforced (tested `AccessError`) |
| View product info in POS | yes | yes | Enforced (tested read allowed) |
| Receive/adjust stock | yes | no | Enforced (tested quant write denied) |
| View stock quantities | yes | no | Enforced — cashier lacks `stock.group_stock_user`, Inventory menu hidden |
| Search/select customers in POS | yes | yes | Enforced (native partner read in POS) |
| Create/edit customers | yes | no | Enforced (tested `AccessError`) — D-004 |
| Manage customer tags/groups | yes | no | Config — native `res.partner.category` ACLs, **not yet tested** |
| View purchase history / insights | yes | limited if enabled | B |
| View customer balance / invoice details | yes | **readable via ACL (gap)** | Gap — POS ACL grants cashier read on `account.move`; no menu, but direct RPC is possible. Tighten in Phase 4 |
| Create invoice from POS | yes | only if enabled | Config — POS `to_invoice` + accounting groups |
| Manage invoices / accounting | yes | no | Enforced for UI (Invoicing menu hidden); ACL read gap above |
| Approve refunds | yes | no | Enforced (tested: backend refund and negative line denied) — D-007 |
| Normal discount | yes | limited by policy | Not offered in Milestone A — D-003 |
| Exceptional discount / price override | yes | no | Config only — `restrict_price_control` is client-side; Gap D-007 |
| View reports | all | own/limited | B |
| Manage users / settings | yes | no | Enforced — no `base.group_system`; tested that a cashier cannot add themselves to Retail Manager |Verified details and gaps (must be handled in Phase 2/4, not assumed solved):
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

### 7.1 Store configuration done in the dev DB (Phase 4, 2026-11-01)

Created through the ORM on `rms` (data, not code — re-create the same way on any new database; steps in
`DEPLOYMENT.md` §11):

| Item | Value |
|---|---|
| Cash journal | `Cash` (`CSH`), type cash, default account `101501` |
| POS payment method | `Cash`, `is_cash_count = True` |
| POS config | `Main Register`: payment `Cash`, `restrict_price_control = True` (manager-only price edits), `cash_control = True`, picking type `PoS Orders` |
| Owner user | `admin` added to `retail_management.group_retail_manager` |

**Verified POS → stock/accounting (ORM, `rms`):** session opened, order `Main Register - 000001` paid
with cash 1.50, `_create_order_picking()` produced a **done** outgoing `PoS Orders` picking and the
quant went **10 → 9**. A manager refund line (qty −1) is accepted. Not yet verified: the real browser
POS UI, receipt printing, barcode scanner, session closing/cash difference — those stay Milestone C
(Phase 8) because they need hardware or a human at the register.

**Superuser rule:** the retail guards allow `env.is_admin()`, so the Odoo administrator can never be
locked out of refunds or receipts while fixing a bad setup (covered by a test).

**Payment methods on `Main Register` (D-017, verified 2026-11-08):** `Cash` (cash journal `CSH`, account
`101501`) plus four mobile wallets, each on its own bank journal so its money is separable:

| Method | Journal | Account | Type |
|---|---|---|---|
| Cash | `CSH` | 101501 | cash |
| Bankak | `BNKK` | 101405 | bank |
| Fawry | `FAWR` | 101406 | bank |
| O-Cash | `OCAS` | 101407 | bank |
| Amen | `AMEN` | 101408 | bank |

Odoo renders each method as a tile using `pos.payment.method.image` (falling back to `money.png` for cash and
`card-bank.png` for bank). The tile icons are the **banks' own artwork**, supplied by the owner and loaded
into the database; no image file is committed to Git. Core caps that field at 50×50
(`pos_payment_method.py:60`), so `models/pos_payment_method.py` redeclares it at **256×256** (D-020): the
tile still draws it at 50 CSS px, the extra pixels only matter on a high-DPI screen or when zoomed.
Before the owner supplied the logos, neutral glyphs drawn locally with PIL were used instead. The
tiles are laid out **two per row with their 50 px icons** by our own
`static/src/pos/payment_methods.scss` (D-019): core declares
`.paymentmethods { grid-template-columns: repeat(2, 1fr) }` but never applies it on desktop because the
template adds `d-flex flex-column`, which stacks all five in one column and pushes the last one out of
view. The same file clamps the due total (`clamp(40px, 6vw, 96px)` over the template's inline 125 px) so a
7-digit SDG amount cannot overflow. The closing dialog lists **every** method with its own
counted/difference, and the session closing entry groups receivables by `payment_method_id`. Caveat
(D-018): a wallet method has no terminal or provider, so tapping it marks the order paid with no proof the
transfer arrived.

The printed receipt keeps Odoo's **QR code** but not the portal URL or the 5-character ticket code
(D-021). The QR encodes `/pos/ticket/validate?access_token=…`, i.e. a direct link to that one sale, so
neither of the other two is needed; they only work together on the portal's manual form (receipt number +
date + code). Our `static/src/pos/receipt.scss` hides `.pos-receipt .unique-code` and `.pos-receipt
.portal-url`; all three are printed by core's `order_receipt.xml:78-92`, where the code is **not**
conditional on the company's "Print" setting, so CSS is the only way to drop it without a template
override.

### 7.2 Country, currency and taxes — Sudan (2026-11-08, D-015)

Odoo 19 Community has **no Sudan localization** (`l10n_sd` does not exist in the image), so the company
keeps the **Generic Chart of Accounts** and the country/currency/tax facts are plain data. Verified
through the ORM on `rms`:

| Setting | Value |
|---|---|
| Country / Fiscal country | Sudan (`base.sd`), both |
| Company currency | SDG (symbol `SDG`; Odoo ships the Arabic `ج.س.` — cached per worker, restart after editing); USD deactivated → SDG is the only active currency |
| Prices | `account_price_include = tax_included` |
| Default taxes | `0% (Sales)`, `0% (Purchase)`, both `price_include_override = tax_included`, amount 0 |
| Tax group | `Taxes` (country Sudan) — created because `account.tax.tax_group_id` is required |
| Register | `Main Register` now in SDG |

Consequences verified: a product priced `100.00` computes `total_included = 100.00` with `0.00` tax;
`compute_all` returns no tax lines above zero. Two Odoo 19 facts worth remembering:
`res.company.currency_id` refuses to change while any `account.move.line` exists, and
`account.tax.country_id` is `@api.depends('company_id')` only — moving the company leaves the old
country on the taxes, so they must be re-pointed (with a matching tax group) by hand.

### 7.3 Product barcode entry — camera widget (2026-11-10, D-022)

Verified facts:

- Core Odoo 19 has a camera barcode dialog: `scanBarcode(env, facingMode)` in
  `@web/core/barcode/barcode_dialog`, backed by `BarcodeDetector` or a ZXing fallback
  (`web/static/src/core/barcode/barcode_video_scanner.js:54-58`). Core exposes it on many2one fields, the
  POS product/orders screens, Events check-in and Attendance — **not** on the product form's `Barcode`
  field, and its many2one button is gated on `isMobileOS()` (`many2one.js:214-217`), so desktop got nothing.
- `product.template.barcode` is `compute='_compute_barcode', inverse='_set_barcode'` — a scanned value
  saves to the single variant exactly like a typed one.
- `retail_management` registers field widget `barcode_scan` (extends `web.CharField`, adds one button into
  `.o_field_input_buttons`) and sets it on `product.product_template_only_form_view`.
- `getUserMedia` needs a **secure context**: `localhost`/`127.0.0.1` or HTTPS. Over `http://<lan-ip>` the
  browser blocks the camera, so the button works on the dev PC but not from a phone on the LAN IP.
- A USB/Bluetooth HID scanner still fills the field with no button: core's background barcode service
  ignores keystrokes aimed at editable elements (`barcodes/static/src/barcode_service.js:90-96`).

## 8. Inventory architecture — verified on `rms_test4` (2026-11-01)

Standard Odoo workflows only; the add-on adds no inventory model. Verified end to end through the ORM:

| Capability | Native mechanism | Evidence |
|---|---|---|
| Product catalog | `product.product`: `name`, `default_code` (internal reference), `barcode`, `categ_id`, `list_price`, `standard_price` (cost), `uom_id`, `is_storable`, `available_in_pos` | Product created as `[COLA-330] Cola 330ml`, barcode `5901234123457`, unit `Units`, cost 0.8 |
| Receive stock | `stock.picking` type `incoming`, `action_confirm` → set `move_ids.quantity` + `picked` → `button_validate` | Picking `WH/IN/00002` done, quant 24 |
| Count / adjust | `stock.quant.inventory_quantity` + `action_apply_inventory()` (field is `groups="stock.group_stock_user"`) | Quant 24 → 22, move `Product Quantity Updated` |
| Movement history | `stock.move` / `stock.move.line` per product | 2 moves, 2 move lines for the test product |
| Low-stock view | `stock.warehouse.orderpoint` (Reordering Rules) — native, usable as the low-stock list | Rule created for the product |
| Barcode | `barcode` field + native barcode lookup (`stock`/`barcodes`); POS scanning is Phase 4 hardware test | Field populated; scanning untested |

**Negative stock (STK-07 decision D-009):** Odoo 19 Community has **no** built-in "block negative
stock" switch (no such setting in `stock/models/res_config_settings.py`; availability checks use
`allow_negative=True` internally). Accepted: negative stock is allowed natively, matching POS behaviour
(POS sells out-of-stock items). Mitigation is the low-stock/reordering-rule view, not a hard block.

**Server-side guard added** (`models/stock_picking.py`): cashiers get `AccessError` from
`button_validate()` **and** `_action_done()` on **incoming/internal** pickings. Outgoing pickings are
deliberately left open because POS validates its own outgoing picking as the cashier
(`pos_order._create_order_picking` → `_action_done`, outside a manager session); blocking those would
silently stop POS stock deduction. Residual: a cashier can still push an outgoing picking via RPC
(D-008). Quant adjustment is blocked at field/ACL level (tested).

`stock.move` in Odoo 19 has **no `name` field** (it is `description_picking` / `inventory_name`);
hand-written ORM snippets must not pass `name`.

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
