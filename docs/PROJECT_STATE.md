# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-11-01 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: **A — Milestone A gate reached (2026-11-01)** · Phases 0–4 done
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
Nothing in progress. Milestone A is implemented and reported; **stopped at the gate for owner approval**
(autonomy 2). Milestone B (invoicing from POS, customers/CRM, dashboard/reports) starts after approval.

## Last completed (newest first, max 8)
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
4. WSL has 3 GB RAM; a full test/install run takes ~8 min. 8 GB recommended.
5. Owner: change the default `admin` password.

## Decisions pending owner review
- D-001 mirror images · D-002 no `pos_hr` · D-003 no discounts · D-004 customers admin-only ·
  D-005 menus use native actions · D-006 no own-orders rule yet · D-007 refunds server-side, price
  config-only · D-008 receipt guard scope · D-009 negative stock allowed · D-010 POS config as data.

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
