# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-11-14 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: **A — Milestone A gate reached (2026-11-01)** · Phases 0–4 done
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
The dev database `rms` is now configured for the owner's store: **Sudan, SDG, 0% taxes, prices tax
included** (D-015). Milestone A is implemented and reported; **stopped at the gate for owner approval**
(autonomy 2). Milestone B (invoicing from POS, customers/CRM, dashboard/reports) starts after approval.

## Last completed (newest first, max 8)
- 2026-11-14: **Portal prints the real invoice, not "فاتورة شكلية"** (D-033) — core's portal renders a
  proforma preview for any invoice without an official PDF attached (`invoice_pdf_report_id`), which made
  paid invoices look like drafts. Posting a customer invoice/credit note now renders the standard report
  and stores it as `invoice_pdf_report_file`; failures are logged, never block posting. Existing invoices
  backfilled on `rms` (all 5 posted ones). Tests: 16, 0 failed (`tests/test_invoice_pdf.py` covers both
  the attach and a render failure). Note `is_move_sent` is untouched, so Odoo still shows "not sent".
- 2026-11-14: **"Paid via <wallet>" on invoices** (D-032) — core printed only `تم الدفع في <date>`, so a
  paid invoice never showed *which* wallet received the money. The payment cell now ends with
  ` باستخدام <journal_name>`; each wallet is its own journal, so renaming a journal renames what prints.
  Verified on `rms` invoice 28 (Bankak journal): `تم الدفع في 14/11/2026 باستخدام Bankak`.
- 2026-11-14: **Document footer** set to `شكراً لزيارتكم · نتشرف بخدمتكم دائماً` — data only, no code:
  `res.company.report_footer` (invoices, edited in **Settings → Companies → Configure Document Layout →
  Footer**) and `pos.config.receipt_footer` (POS receipt, a separate field on the till config). Set on
  `rms` and `rms_test4`; verified printed at the bottom of a rendered invoice.
- 2026-11-14: **`اسم العميل` label on invoices** (D-031) — the recipient block printed with no heading,
  which read as the shop's own details; a bold `اسم العميل` now sits above it. Three xpaths are needed
  because core sets the `address` variable inside three different branches and an xpath matches only
  its first node; put in the invoice template (not `web.address_layout`) so vendor bills and other
  reports keep core's block. Verified: exactly one label in each of the three branches on `rms_test4`
  invoice 1, and on `rms` invoice 28.
- 2026-11-14: **Invoice payment block** (D-030) — customer invoices now print **طرق الدفع**, one line
  per company bank account (`بنكك · رقم الحساب : … · باسم …`) followed by
  `ارسل اشعار الدفع في الرقم واتساب <company phone>`, instead of core's "Payment Communication" line.
  Data lives in the database, not in code; `views/company_bank_accounts.xml` adds the **Invoices** page
  to the company form (bank accounts + the two wordings `rms_payment_title` / `rms_payment_note`) so
  nothing needs a code edit. Verified by rendering invoice 1 of `rms_test4` (styled HTML) and invoice
  28 of `rms` (styled HTML). The owner has since entered the real wallets on `rms`
  (`بنكك` 00000000, `فوري` 00000000, holder `اسم صاحب الحساب`), so `rms` prints all of it. Also on
  2026-11-14: the POS "Save as PDF" button was removed
  (D-028 reversed, owner's call) and the receipt print CSS was reduced to `@page { margin: 0 }` so
  the browser header/footer stay hidden without moving the ticket (D-029).
- 2026-11-13: **POS receipt gets a "Save as PDF" button** (D-028) — inherited template only, reuses
  core `doFullPrint`, so `nb_print` counting and the printer fallback stay native. Next to it, the
  **Inventory app tile now opens the plain stock list** (`stock.action_view_quants`) instead of the
  Overview cards, at the owner's request (D-027); `views/inventory_app_default.xml` is the only file.
  Verified: the tile href became `/odoo/stock-locations` and renders a list; the POS asset bundle
  rebuilt with our template inside and the `hasclass` selector resolves to exactly one button (lxml
  check against the core template). **Not verified visually:** the POS UI does not render in the
  automated browser (blank page on `/pos/ui/13/login` even on a fresh config), so the button was not
  clicked — the owner should confirm on the receipt screen.
- 2026-11-10: **Verified from scratch**: cloned the repo to `/tmp/rms-clone`, ran `scripts/setup.sh dev`
  (correct `.env` + `config/odoo.conf`), and `docker compose config` validates — so a stranger can start
  from the README. Then a **clean install on a brand-new disposable database** (`rms_ci`): module installs,
  **14 tests, 0 failed / 0 errors**. That test caught a real bug: the `path = "apps"` added to the launcher
  action minutes earlier **breaks any fresh install** ("Path to show in the URL must be unique!" — core's
  Apps action owns `apps`), so the field was removed (D-025 corrected); the launcher URL stays
  `/odoo/action-retail_management.action_apps_page`, verified rendering in the browser.
- 2026-11-10: **Repo prepared for publishing** (D-026): LGPL-3 `LICENSE`, a product `README.md` (features,
  requirements, quick start, tests, layout, variants, deployment, license), and
  `docs/INDUSTRY_VARIANTS.md` (one base module + thin per-industry add-ons, configuration before code,
  what must never be copied into a variant). Secret scan of all 53 tracked files: `.env` and
  `config/odoo.conf` are ignored and untracked, templates hold only placeholders, no keys, dumps, customer
  data or brand logos. Repo renamed **odoo-rms** in the README and the module author set to
  `odoo-rms contributors`. **Nothing was pushed** — the repo still has no remote; publishing is the owner's
  decision (Hard stop).
- 2026-11-10: **Opening the app** (D-025). Users install it from the browser as a **PWA** (desktop /
  home-screen icon, full screen) instead of an OS installer. Two gaps closed: the module only had
  `static/description/icon.png`, so an installed app got Odoo's purple logo — added
  `static/description/icon.svg` and the scoped manifest now serves our green shop icon; and the launcher
  action had no `path`, so `/odoo/apps` did not open it — added `path = "apps"`. Verified in the browser:
  `/scoped_app?app_id=retail_management&path=apps` returns title *Install Retail Management* plus icon links;
  the manifest returns `name: Retail Management`, `display: standalone`. **Owner confirmed the install works on
  his own Chrome** (2026-11-10): icon on the address bar → Install → app window with no address bar. Install
  needs **HTTPS or `localhost`** (`127.0.0.1` counts). Remaining nit: the install URL the owner used first was
  `/odoo/point-of-sale/apps`, so a reinstall should be done from `/odoo/apps` or the `scoped_app` URL above to
  land on the launcher.
- 2026-11-10: **Alert: the burger reordering rule had been deleted** by Odoo's auto-vacuum, which removes
  manual rules created by the system user (uid 1) when nothing is to order (`stock_orderpoint.py:657-671`).
  Recreated as `admin` (rule id 3, min 10 / max 50) and proved it survives an explicit
  `_unlink_processed_orderpoints()` call. **Any rule an agent creates through `odoo shell` will vanish
  overnight** — create rules from the UI or with `with_user(<real user>)`.
- 2026-11-10: **Arabic activated** as `ar_001` (generic Arabic, RTL) next to English (D-024). No `ar_SD` exists
  in Odoo 19, so this is the only complete Arabic. Verified `ar001.direction == "rtl"` and, in a browser on
  `rms_test4`, a fully right-to-left UI in Arabic. `admin` stays on English; each user switches in
  Preferences. Gotcha recorded: the installed-language list is cached per worker, so **restart `odoo` after
  activating a language**, else the UI silently stays English.
- 2026-11-10: **Low-stock warning** set up as native reordering rules with `trigger = "manual"` (D-023): one
  rule on `burger` (WH/Stock, min 10, max 50) as the example; the board is **Inventory → Operations →
  Replenishment** with the **"To Reorder"** filter. Nothing blocks a sale — the owner chose this over a
  custom zero-stock block (native Odoo 19 Community has no such setting, verified). Min/max numbers are
  placeholders; the owner still has to give real ones per product.
- 2026-11-10: **Camera Scan button on the product form's Barcode field** (D-022). New field widget
  `barcode_scan` (`static/src/fields/barcode_scan_field.{js,xml}`) reuses core's `scanBarcode(env)` dialog and
  writes the result with `record.update`, then plays a short **beep** (2200 Hz oscillator, one page-wide
  `AudioContext` created in the click because Chrome only starts audio after a gesture); core has no barcode
  sound of its own. `views/product_barcode_scan.xml` sets it on `product.product_template_only_form_view`.
  Verified: 14 tests green on `rms_test4`, widget + beep code present in the generated `web.assets_backend`
  bundle, and in a browser the button renders at the right of the Barcode input, opens the "Barcode Scanner"
  dialog, and an `AudioContext` created the same way reports `state === "running"`. `rms` upgraded and
  `odoo` restarted. Limit: template form only, and the camera needs `localhost` or HTTPS.
- 2026-11-08: Receipt now prints **QR only** (D-021): the portal URL and the 5-character code are hidden by
  `static/src/pos/receipt.scss`. Core's company setting can remove the URL but not the code, which is
  unconditional in `order_receipt.xml:78-92`. Verified the rule is in the loaded POS bundle and both children
  of `.pos-receipt` compute `display: none`; the QR still points at that sale's ticket.
- 2026-11-08: Raised the payment icon storage cap from Odoo's 50×50 to **256×256** (D-020) because the owner
  said the brand logos looked low quality. `models/pos_payment_method.py` redeclares the field in an
  `_inherit` model — verified `_fields['image'].max_width == 256` and the four icons now stored as 256×256
  PNGs (were 50×50), still drawn at 50 CSS px in the till with no scrollbar. **Waiting on the owner**: new,
  simpler artwork (symbol only) to load with the same script; a 50 px tile cannot carry the small text in
  the bank badges regardless of storage size.
- 2026-11-08: Payment tiles now show the **banks' own icons** (Bankak, Fawry, O-Cash, Amen), supplied by the
  owner from `banks-icons/`. Corners flood-filled transparent, resized, stored in `pos.payment.method.image`
  — which Odoo caps at 50×50 px, so the till shows 50 px icons. Nothing committed to Git (the images live in
  the database). `write()` blocks fields other than `sequence` while a session is open, so the image was
  written through the base ORM `write`; the owner's open session was not closed.
- 2026-11-08: POS payment methods in **two columns with full 50 px icons** (D-019), so all five fit with no
  scrollbar (owner's screenshot showed the last one cut off). New `static/src/pos/payment_methods.scss` in
  `point_of_sale._assets_pos`; core's own 2-column rule never applied because the desktop markup adds
  `d-flex flex-column`. Measured on the desktop branch: 400 px pane, two 186 px columns, 3 rows of 58 px,
  block needs 181 px, `scrollHeight == clientHeight`. Group headers were built and removed — they cost the
  row that made it fit. Same file also clamps the due total, which Odoo hardcodes at 125 px and which clipped
  a 7-digit SDG amount.
- 2026-11-08: Four **mobile-bank payment methods** added to `Main Register` (D-017): Bankak, Fawry, O-Cash,
  Amen, each with its own bank journal (`BNKK`/`FAWR`/`OCAS`/`AMEN`, accounts 101405–101408) and a locally
  drawn icon; Cash stays first. Verified in the register: 5 tiles with icons, the closing dialog shows a
  Counted/Difference line per method, and the test session closed with 0 orders / 0 journal entries.
  Recorded the trust-on-the-cashier risk of wallet payments as D-018.
- 2026-11-08: Cash-difference guard on `Main Register` (D-016): *Set Maximum Difference* on, limit
  **10,000 SDG** (≈ 1 USD). A cashier cannot close a session whose counted cash is off by more, a manager
  must accept it. Verified in the Odoo 19 source (`closing_popup.js` + `pos_session._load_pos_data`) and in
  the Settings UI (switch checked, amount stored on the register).
- 2026-11-08: Store configured for **Sudan** (D-015): country + fiscal country Sudan, company currency
  **SDG** (USD deactivated), prices **tax included**, the four generic taxes at **0%** and price-included.
  No Sudan localization exists in Odoo 19, so the generic chart stays. Verified through the ORM
  (100.00 → total 100.00, 0.00 tax; `Main Register` in SDG) and on the Invoicing Settings page
  (Sudan / SDG / `0% (Sales)` / Tax Included). The 2 leftover test POS sales were deleted with the
  owner's approval to unlock the currency change; the DB is back to 0 orders, 0 sessions, 0 journal items.
  Afterwards the demo catalogue (43 products) was converted from dollar-era figures to SDG at the owner's
  rate of **10,000 SDG = 1 USD** (`Whiteboard Pen` 1.20 → 12,000, `Two-Seat Sofa` 1,500 → 15,000,000),
  prices and costs both scaled. No pricelist had fixed prices, so nothing else needed touching.
  The currency symbol was then changed from the Arabic `ج.س.` to **`SDG`** (owner request), so every amount
  now reads `12,000.00 SDG`. Gotcha: `res.currency` symbols are cached in the worker, so the server must be
  restarted before the change shows up in the browser.
- 2026-11-07: App switcher is now a **full-page icon launcher** like Odoo 16–18 (D-014): client action
  `retail_management.apps_page` + navbar button (`apps_button.xml`), search box, icon tiles, gradient
  background. Replaces the dropdown grid from D-013. Verified in a browser: 7 tiles with icons, live
  search filter, tile navigation; tests 13/0 failed.
- 2026-11-03: App switcher restored as an **icon grid** (owner request): new
  `static/src/xml/apps_grid.xml` inherits `web.NavBar.AppsMenu` (no core change), styling in
  `static/src/scss/apps_grid.scss`, and Retail Management got an app icon (D-013). Verified in a
  browser: 7 apps with icons, clicking navigates; tests still 13/0 failed.
- 2026-11-03: Discuss app hidden (mail cannot be uninstalled — dependency of Contacts/Stock/Invoicing).
  Root menu restricted to `group_no_discuss`; verified admin no longer sees it (D-011).
- 2026-11-01: Phase 4: dev DB configured (`Main Register`, cash journal/payment method, manager-only price
  edits, cash control); POS sale verified end to end through the ORM (order paid, picking done, stock
  10 → 9, manager refund accepted). Docs: `ARCHITECTURE.md` §7.1, `DEPLOYMENT.md` §11, D-010.
- 2026-11-01: Phase 3: native product/stock flows verified (receipt, adjustment, movement history,
  reordering rules); cashiers blocked from receiving/moving stock (D-008); negative stock accepted
  natively (D-009); 13 security tests pass.
- 2026-11-01: Phase 2: `group_retail_cashier` / `group_retail_manager` mapped onto verified native groups
  (no `base.group_system`); server-side refund guard; permission matrix in `ARCHITECTURE.md` §6.2/§6.3.
- 2026-11-01: Phase 1: `retail_management` module + Retail Management menu pointing at native actions;
  clean install/upgrade/uninstall verified.
- 2026-11-01: Owner approved Milestone A and delegated the open choices → D-002…D-005.
- 2026-11-01: Phase 0 discovery + Stage 0 environment (Docker Desktop, Odoo 19.0-20261015).

## Next action (concrete)
**Owner:** try the new Scan button. *Retail Management → Products →* open a product (or **New**) *→* the
**Barcode** field has a barcode icon at its right edge. Click it, allow the camera when Chrome asks, hold a
product barcode in front of the webcam — the field fills with the digits (nothing is saved until **Save**).

**Owner:** run the Milestone A acceptance scenarios in the browser at http://localhost:8069:
1. Log in as the Retail Manager; open *Retail Management* → *Point of Sale* → *Main Register* → *Open*.
2. Sell a product for cash, check the receipt, then close the session (cash counted).
3. Log in as a Retail Cashier: confirm only *Point of Sale* and *Products* appear and a refund is refused.
4. Report anything that feels wrong about the flow (this is the Milestone A acceptance).

**After approval**, Milestone B starts with invoicing from POS and the Customers/CRM screens.

## In-flight / uncommitted work
None (Phase 4 committed and tagged `phase-4-done`).

## Blockers and questions for the owner
1. **Milestone A gate**: accept the working core or list changes.
2. D-002…D-010 are Tier 2 decisions, implemented and reversible; listed in the report.
3. D-001: prod images still need a mirror/VPN in this country before Phase 8 deployment.
4. WSL has 3 GB RAM; a full test/install run takes ~8 min. 8 GB recommended. The PostgreSQL container
   has already recovered once from an unclean shutdown after the memory ran out — a crashed dev DB is a
   reminder, not a data loss so far, but give WSL more memory before any long run.
5. Owner: change the default `admin` password.
6. Owner: the company is still called **My Company** (no shop name yet) and the products are Odoo's demo
   items, now priced in SDG at 10,000 per USD — the catalogue needs your real items and prices before the
   register goes live. Note: some demo items have a *cost* above their *sale price* (e.g. `Large Cabinet`
   costs 8,000,000 and sells for 3,200,000) because Odoo's demo data was never consistent; real costs fix it.

## Decisions pending owner review
- D-001 mirror images · D-002 no `pos_hr` · D-003 no discounts · D-004 customers admin-only ·
  D-005 menus use native actions · D-006 no own-orders rule yet · D-007 refunds server-side, price
  config-only · D-008 receipt guard scope · D-009 negative stock allowed · D-010 POS config as data ·
  D-011 Discuss hidden · D-012 Contacts hidden · D-013 icon-grid app switcher (template inherit) ·
  D-014 full-page app launcher (supersedes D-013) · D-015 Sudan / SDG / 0% included taxes ·
  D-016 cash-difference guard 10,000 SDG · D-017 four wallet payment methods · D-018 wallet payments are
  trust-on-the-cashier · D-022 camera Scan button on the product Barcode field · D-023 low-stock reordering rules · D-024 Arabic (ar_001).

## Environment quick facts (full detail: `ARCHITECTURE.md` §2)
- Project: `~/rms` in WSL Ubuntu 24.04 · Windows copy is a backup only
- Dev URL: http://localhost:8069 · Start: `docker compose up -d` · Logs: `docker compose logs -f odoo`
- Odoo 19.0-20261015 · PostgreSQL 16.15 · Python 3.12.3
- Install/upgrade: `docker compose run --rm odoo odoo -d <db> -i|-u <module> --stop-after-init`
- Tests (to verify in Phase 1): `docker compose run --rm odoo odoo -d rms_test -i <module> --test-enable --stop-after-init`
- Dev DB: `rms` · disposable test DBs: `rms_test*`

## Known issues / tech debt
- Docker Hub CDN geo-block → mirror workaround (D-001). `scripts/bootstrap.sh dev` uses `.env` tags.
- Empty `custom_addons/` makes Odoo skip `/mnt/extra-addons` (expected; fixed once a module exists).

## Recent session log (rolling, last 10 — newest first)
| Date | Agent/tool | What happened |
|---|---|---|
| 2026-11-01 | OpenCode / deepseek-v4.1-flash-free | Phase 2: retail groups, server-side refund guard, permission matrix, 10 security tests green |
| 2026-10-31 | OpenCode / deepseek-v4.1-flash-free | Repo copied to `~/rms`; Docker engine confirmed on Windows, Ubuntu integration off; stopped |
| 2026-10-31 | OpenCode / deepseek-v4.1-flash-free | Stage 0 preflight failed (path + Docker integration); baseline committed |
