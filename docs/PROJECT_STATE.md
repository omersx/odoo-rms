# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-11-08 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: **A — Milestone A gate reached (2026-11-01)** · Phases 0–4 done
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
The dev database `rms` is now configured for the owner's store: **Sudan, SDG, 0% taxes, prices tax
included** (D-015). Milestone A is implemented and reported; **stopped at the gate for owner approval**
(autonomy 2). Milestone B (invoicing from POS, customers/CRM, dashboard/reports) starts after approval.

## Last completed (newest first, max 8)
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
  D-014 full-page app launcher (supersedes D-013) · D-015 Sudan / SDG / 0% included taxes.

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
