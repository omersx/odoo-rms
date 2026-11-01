# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-11-01 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: A · Phase: 2 (roles and security) · Status: **Phase 2 complete**
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
None in progress. Next is Phase 3 (products and inventory). Roles, groups, refund guard and tests are
in place (D-005…D-007).

## Last completed (newest first, max 8)
- 2026-11-01: Phase 2: `group_retail_cashier` / `group_retail_manager` mapped onto verified native
  groups (no `base.group_system`); refund guard server-side (`pos.order._refund`, `pos.order.line`
  `qty < 0`); permission matrix reality check in `ARCHITECTURE.md` §6.2/§6.3; 10 security tests pass.
- 2026-11-01: Phase 1: `custom_addons/retail_management` created (manifest + Retail Management menu with
  six items pointing at native actions). Clean install and upgrade on `rms_test2`; uninstall leaves no
  leftover XML IDs or menus. Menu visibility verified per group.
- 2026-11-01: Owner approved Milestone A and delegated the open choices → D-002 (no `pos_hr`),
  D-003 (no discounts in MVP), D-004 (customers admin-only), D-005 (menus use native actions).
- 2026-11-01: Phase 0 discovery finished: 692 modules (Community-only); dependency chain
  `point_of_sale → stock_account → stock + account`; POS offline (IndexedDB) and extension points.
- 2026-11-01: Stack verified: `http://localhost:8069/web/login`; Odoo 19.0-20261015, PostgreSQL 16.15,
  Python 3.12.3; image geo-block worked around (D-001).

## Next action (concrete)
Start Phase 3 (products and inventory):
1. Create the test scenario in a fresh disposable DB: `docker compose run --rm odoo odoo -d rms_test5 -i retail_management --stop-after-init`.
2. Check which product fields/views are already usable for retail (categories, price, cost, unit,
   barcode, internal reference) — prefer native views, add a view only for a verified gap.
3. Verify stock operations natively (receipt, adjustment/count, movement history, low-stock view) and
   the negative-stock policy (STK-07) — decide and document it in `DECISIONS.md`.
4. Add tests for any guard added; record scenario A and D evidence in the roadmap.

## In-flight / uncommitted work
None.

## Blockers and questions for the owner
1. D-002…D-007 are Tier 2: implemented and reversible; listed for your review in the report.
2. D-001: dev images come from `mirror.gcr.io` because Docker Hub's CDN blocks this country.
   Production will face the same block (VPN/proxy or approved mirror needed).
3. WSL sees only 3 GB RAM (warning) — a full test run takes ~8 min. 8 GB recommended.
4. Owner: log in as `admin` and change the default password before any shared/network use.

## Decisions pending owner review
- D-001 — `mirror.gcr.io` for official images in this region (same digests).
- D-002 — no `pos_hr`; one Odoo user per cashier.
- D-003 — no discount button / `pos_discount` in Milestone A.
- D-004 — customers created by Administrators only; cashiers select existing ones in POS.
- D-005 — Retail Management menus point at native actions with native groups.
- D-006 — no "own POS orders only" rule yet (would break session totals); Phase 4.
- D-007 — refund enforced server-side; price override is config-only (residual client-side gap).

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
