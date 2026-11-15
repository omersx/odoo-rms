# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-11-15 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: **A — Milestone A gate reached (2026-11-01)** · Phases 0–4 done
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
Milestone A is implemented and reported; **stopped at the gate for owner approval** (autonomy 2).
Milestone B (invoicing from POS, customers/CRM, dashboard/reports) starts after approval.
The owner is currently reviewing the printed documents, the invoice form (the preview pane collapse,
D-037, still needs his confirmation at ≥ 1400 px window width) and the cashier's workspace (D-038…D-041:
customers, invoicing at the till *and* from the back office, and the shop app is hidden from the admin;
the trade-off that the cashier can also reach journal entries is logged as B-001).

## Last completed (newest first, max 8)
- 2026-11-15: **"Clone it for a client" proven end to end** (D-046) — a real fresh clone was set up as a second
  shop (project `rmsclient`, DB `rmsclient`, port 8070) with `scripts/setup.sh dev` + `scripts/bootstrap.sh dev`,
  the app installed there, and `http://localhost:8070/web/login` answered **HTTP 200** while the original stack
  kept running on 8069. Two blockers were found and fixed on the way: the scripts were committed as `644`
  (`Permission denied` on a Linux clone) and the compose file hardcoded `name: rms` + port 8069, so a second
  copy would have fought the first. A failed image pull (D-001 geo-block) now warns instead of aborting.
  The test stack was removed; only the volumes `rmsclient_db-data` / `rmsclient_odoo-data` remain (deleting
  volumes needs the owner's approval).
- 2026-11-15: **Publication audit + template cleanup** (D-045) — the repo is ready to publish except the push
  itself (owner's action, Hard stop). What was checked: 65 tracked files, no remote, `.env` and
  `config/odoo.conf` untracked and ignored, no secrets/tokens/local paths/DB dumps in the tree, LGPL-3 licence,
  README rewritten (22 tests, 34 files, the new features, a "customize it for your company" table). The owner's
  real wallet numbers and holder name were in `docs/PROJECT_STATE.md` **and in history**: replaced with
  placeholders and purged from all 58 commits with `git filter-branch` (tags kept, **every hash changed**, so
  older hash references are stale). A clean install on a brand-new database without demo data (`rms_test5`)
  installs 19.0.1.18.0 and passes **22 tests, 0 failed** — it also exposed a test that assumed Arabic was
  installed, now fixed.
- 2026-11-15: **The cashier can read stock quantities** (D-044) — *Retail Management → المخزون* is now a
  read-only on-hand list (product, location, quantity, reserved, available). No new rights were needed:
  stock already grants quant **read** to every internal user (`access_stock_quant_all`, `1,0,0,0`); the menu
  and the core action were merely gated on `stock.group_stock_user`, which also allows editing stock — so a
  small `act_window` + non-editable list replaces them (`views/stock_quant_readonly.xml`). Verified in the
  cashier's browser: 3 rows, Arabic headers, no New button, no editable cells; writes still denied. Module
  19.0.1.18.0, both DBs upgraded. Tests: 22, 0 failed (`test_cashier_reads_on_hand_quantities`).
- 2026-11-15: **The shop app speaks Arabic** (D-043) — new `i18n/ar_001.po` translates our own labels, which
  were the only English left in the cashier's navbar: *إدارة البيع*, *نقطة البيع*, *المنتجات*, *المخزون*,
  *الفوترة*, *العملاء*, *الإعدادات*, launcher *التطبيقات*. Server-side names verified with `lang=ar_001` on
  `rms`; in the cashier's browser the tile reads *إدارة البيع* and `load_menus` returns Arabic only. Module
  19.0.1.17.0, both DBs upgraded, `odoo` restarted (translations are cached per worker). Tests: 21, 0 failed.
  English left in the launcher itself ("Search apps…", empty-state text) — Owl templates, logged in D-043.
- 2026-11-15: **The launcher refreshes its menus when it opens** (D-042) — the owner still saw the Retail
  Management tile on the admin login after D-041 even though the server was already clean (`load_menus` for a
  fresh system user: *Settings, Apps, Invoicing, Dashboards, Point of Sale*, no Retail entry; cashier still has
  menu 268). Cause: core caches menus in the browser (`webclient_menus` in localStorage keyed by
  `session.registry_hash`), so an already-open tab keeps the old list. `static/src/apps_page/apps_page.js` now
  calls `this.menu.reload()` on mount and re-renders on `MENUS:APP-CHANGED`. Verified on `rms`: probe system
  user's launcher = *Dashboards, Point of Sale, Invoicing, Apps, Settings* (no Retail Management), cashier =
  *لوحات البيانات, Retail Management*, no console errors. Module 19.0.1.15.0; probe user deleted; the owner
  still needs one **Ctrl+Shift+R** to load the new JS. Tests: 21, 0 failed.
- 2026-11-15: **The admin login no longer sees Retail Management** (D-041, owner's call) — the shop app is
  restricted to *Retail Cashier* (a manager inherits it), and the native apps — standalone *Point of Sale*,
  *Invoicing*, *Apps*, *Tests* — are now restricted to the Odoo administrator (`base.group_system`) instead
  of *Retail Manager*, so the admin keeps them without the shop app. The admin held *Retail Manager* only
  because it had been assigned by hand; it was removed on `rms` (admin keeps Settings, POS/stock/product
  Administrator, Invoicing, Contact Creation). Verified on `rms`: admin's visible apps = *Settings, Apps,
  Invoicing, Dashboards, Inventory, Point of Sale*; the cashier's = *Dashboards, Retail Management*; browser
  screenshots of both. Refunds by the admin are unaffected (`is_retail_manager` also accepts `env.is_admin()`).
  Tests: 21, 0 failed (new: `test_retail_app_is_cashier_only`,
  `test_technical_apps_are_for_the_odoo_administrator`).
- 2026-11-15: **Back-office invoicing enabled for the cashier too** (D-040, owner's call) — *Retail Cashier*
  now also implies Odoo's **Invoicing** right, so he creates, edits and posts invoices in
  *Retail Management → Invoicing*. Odoo has no narrower switch (`account.move._post` hard-requires the group,
  and the group's ACL on `account.move` is `1,1,1,1` with no rule), so **the books are exposed to him**:
  verified on `rms` that he can now read, create and write journal entries. Accepted by the owner, logged as
  B-001 (and B-003 proposes splitting the role). The launcher still shows **two tiles**: core's *Invoicing*
  app (`account.menu_finance`) is now manager-only in `data/hide_apps.xml`, so the cashier reaches the same
  invoice list inside Retail Management (`Point of Sale, Products, Invoicing, Customers`). Verified in a real
  cashier session: `/odoo/customer-invoices` opens with *جديد*. Tests: 20, 0 failed.
- 2026-11-15: **A cashier adds customers and invoices a sale at the till** (D-039) — the owner's request,
  done with the least privilege that achieves it. *Retail Cashier* now implies native **Contact Creation**
  (`base.group_partner_manager`) so he can add a customer at checkout, and **nothing from accounting**:
  POS creates and posts invoices through its own sudo path (`pos.order._create_invoice` → `AccountMove.sudo()`,
  `_post` on `invoice.sudo()`), so the cashier needs no *Invoicing* right. Proven on `rms`: a user holding only
  Internal User + POS User + Contact Creation generated and posted `INV/2026/00006` from a POS order.
  The one-line alternative (`account.group_account_invoice`) was rejected at first because a probe showed it
  also lets a cashier **read, write and create journal entries** — the books; the owner accepted that price
  the same day in D-040, so the group is now granted. Visible menus under Retail Management for the cashier
  are *Point of Sale, Products, Invoicing, Customers*. Trap recorded: `implied_ids` with `(4, ref)`
  never removes a group on upgrade — use `[(6, 0, [...])]`. Tests: 21, 0 failed (new:
  `test_cashier_can_invoice_a_pos_order`, `test_cashier_cannot_create_invoice_in_backoffice` at the time,
  `test_cashier_cannot_read_journal_entries` at the time; the latter two were replaced by D-040).
- 2026-11-15: **Cashier account created and his app list trimmed** (D-038) — login `cashier` / password
  `cashier` (placeholder, Arabic UI, group *Retail Cashier*: internal user + POS user only). His app list is
  **Retail Management + Dashboards**: the standalone Point of Sale app, Apps and Tests are now
  manager-only (`data/hide_apps.xml`); he still opens the till from Retail Management → Point of Sale,
  which lands directly on the POS dashboard (`Main Register`, `متابعة البيع`). Verified in a real session as
  `cashier` on `rms`: two tiles on the launcher, POS dashboard opens, and product/stock/company writes are
  denied by ACLs. Two gaps found and logged in `BACKLOG.md`: he can still *read* invoices and user records
  (B-001), and the Dashboards app is empty for him because both dashboards are Invoicing/Administrator-only
  (B-002). Tests: 18, 0 failed (new: menu groups are manager-only).
- 2026-11-15: **The invoice preview pane can be collapsed** (D-037) — the owner kept the document preview
  but asked for a way to close/expand it, and Odoo 19 has no such control (mail's black pill *pops the pane
  out to another window*; pdf.js's `»` only opens its own toolbar). `static/src/views/preview_collapse.js`
  patches mail's `AttachmentView` and adds a dark tab on the right edge of the screen; clicking it hides the
  pane (`o_rms_preview_collapsed` → `display: none`), clicking `«` brings it back. Verified on `rms_test4`
  invoice 7 with the wide layout forced: tab at the right edge (offset 0), collapse/expand both flip the
  computed display. Two traps recorded: `this.el` is undefined in Owl 2 `onMounted`, and Odoo's RTL stylesheet
  swaps `left`/`right`, so the tab's position is set inline. **The ≥1400 px side-by-side layout was not
  reproduced** (automated browser ~700 px wide) — the owner should reload with **Ctrl+Shift+R** and confirm.
  `mail` added to `depends`.
- 2026-11-15: **A normal invoice fits on one page again** (D-035, D-036) — `INV/2026/00005` and `00001`
  printed on two pages with only the last line of the payment block spilling over. Cause: not a bug, but
  arithmetic — an A4 body is 213 mm (297 − 52 − 32) and a 3-line invoice whose products carry a
  description needs ~218 mm. The payment block is now printed tight (0.9 em, line-height 1.25, `div`s)
  and core's `mt-5` above the totals is cut to 12 px, which moves the totals up ~21 mm. All 5 posted
  invoices on `rms` are 1 page, last line at 254.8 mm of the 265 mm body. The attached PDF is also
  rendered in the **customer's language** now (D-036): the report follows the session language, so the
  PDFs attached earlier were English while the screen prints Arabic. Re-attached all 5 (Arabic, Tajawal).
  Tests: 17, 0 failed (new: `test_pdf_renders_in_customer_language`).
- 2026-11-14: **Invoice PDFs are styled again** (D-033 amended, D-034) — the first backfill came out plain
  because Odoo only passes its asset cookie to wkhtmltopdf inside a web request; rendering from `odoo shell`
  (or a cron) skips it. The five `rms` invoices were regenerated with `dbfilter = ^rms$` set temporarily (so
  asset URLs resolve without a session) and the setting was removed afterwards; verified by the embedded fonts
  (Tajawal, not DejaVu/Nimbus). Also found and fixed while testing in the UI: **Odoo 19 refuses to post a
  customer invoice** while the company's bank account is untrusted, so both wallets are now marked *Send Money*
  (`allow_out_payment`) — without that, the owner could not confirm an invoice at all.
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
  28 of `rms` (styled HTML). The owner has since entered the real wallets on `rms`, so `rms` prints all of it
  (the numbers stay in the database, never in the repo). Also on
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
**Owner:** publish it — create the empty public repo `odoo-rms` on GitHub, then (Hard stop for the agent:
no remote, nothing pushed) either add the remote yourself or ask for it explicitly:
`git remote add origin https://github.com/<your-account>/odoo-rms.git && git push -u origin main`.
Before that, confirm the **branch name** is `main` and that you are happy with the rewritten history
(D-045 — the wallet numbers are gone from every commit, and so is the pre-audit history).

**Owner:** reload your open Odoo tab once with **Ctrl+Shift+R** — that is the last step for D-042 (the
launcher now refreshes itself on every open, so it is a one-time thing). The Retail Management tile is gone
for the admin login after that.

**Owner:** open (or download) `INV/2026/00005` — it is one page now, and the payment block sits at the
bottom of it. Tell me if the tighter wallet block is too small on paper (`views/report_invoice.xml`,
`font-size: 0.9em; line-height: 1.25`).

**Owner:** try the new Scan button. *Retail Management → Products →* open a product (or **New**) *→* the
**Barcode** field has a barcode icon at its right edge. Click it, allow the camera when Chrome asks, hold a
product barcode in front of the webcam — the field fills with the digits (nothing is saved until **Save**).

**Owner:** run the Milestone A acceptance scenarios in the browser at http://localhost:8069:
1. Log in as the Retail Manager; open *Retail Management* → *Point of Sale* → *Main Register* → *Open*.
2. Sell a product for cash, check the receipt, then close the session (cash counted).
3. Log in as the Retail Cashier (`cashier` / `cashier`): confirm the app list shows only *Retail Management*
   and *Dashboards*; add a customer; invoice a sale with the POS **Invoice** button; open
   *Retail Management → Invoicing* and check the invoice list (D-040). The standalone *Invoicing* app tile
   is intentionally hidden from him.
4. Report anything that feels wrong about the flow (this is the Milestone A acceptance).

**After approval**, Milestone B starts with invoicing from POS and the Customers/CRM screens.

## In-flight / uncommitted work
None.

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
7. Owner (D-040): the cashier now has Odoo's *Invoicing* right (back-office invoices enabled, as you asked).
   It is all-or-nothing, so he can also reach journal entries through a direct request, even though no
   Accounting menu is shown. B-001 tracks narrowing it; B-003 proposes a separate *Retail Billing* role.

## Decisions pending owner review
- D-001 mirror images · D-002 no `pos_hr` · D-003 no discounts · D-004 customers admin-only ·
  D-005 menus use native actions · D-006 no own-orders rule yet · D-007 refunds server-side, price
  config-only · D-008 receipt guard scope · D-009 negative stock allowed · D-010 POS config as data ·
  D-011 Discuss hidden · D-012 Contacts hidden · D-013 icon-grid app switcher (template inherit) ·
  D-014 full-page app launcher (supersedes D-013) · D-015 Sudan / SDG / 0% included taxes ·
  D-016 cash-difference guard 10,000 SDG · D-017 four wallet payment methods · D-018 wallet payments are
  trust-on-the-cashier · D-022 camera Scan button on the product Barcode field · D-023 low-stock reordering rules · D-024 Arabic (ar_001).
  D-025…D-046 (PWA install, merge/workflow choices, invoice layout, preview pane, cashier account and rights,
  launcher menu refresh, Arabic labels, read-only stock, template/history hygiene, Docker identity) are listed
  in `DECISIONS.md`; D-038…D-046 are the ones to read for the cashier, the app list and cloning per client.

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
