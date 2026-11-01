# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-11-01 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: A · Phase: 0 (discovery) · Status: **Phase 0 complete — at the owner gate**
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
Nothing in progress. Phase 0 is finished and reported; **no application code exists yet**. Phase 1
(Milestone A implementation) starts only after the owner approves the gate report and the plan.

## Last completed (newest first, max 8)
- 2026-11-01: Phase 0 discovery finished: 692 modules (Community-only); dependency chain
  `point_of_sale → stock_account → stock + account`; real groups/ACLs read from `rms_test`;
  POS offline (IndexedDB) and extension points documented — `ARCHITECTURE.md` §4, §6.1, §7, §12.
- 2026-11-01: `rms_test` created with `point_of_sale,pos_hr,contacts` (67 modules).
- 2026-11-01: Stack verified: `http://localhost:8069/web/login` → HTTP 200; Odoo 19.0-20261015,
  PostgreSQL 16.15, Python 3.12.3; `rms` DB (base only, no demo).
- 2026-11-01: Docker Hub blob CDN is geo-blocked (`403 … block access from your country`); pulled the
  same official images from `mirror.gcr.io` (digests identical), set them in `.env` (D-001).
- 2026-11-01: Fixed Odoo 19 CLI incompatibility: `--without-demo=all` → `--without-demo` in
  `scripts/bootstrap.sh` and `docs/DEPLOYMENT.md`.
- 2026-11-01: Project copied to `~/rms`; Stage 0 facts recorded in `ARCHITECTURE.md` §2.

## Next action (concrete)
**Owner decision required.** After approval, Phase 1 starts with:
1. Create `custom_addons/retail_management/` with a minimal manifest
   (`depends = ['point_of_sale', 'stock', 'account', 'contacts']`, version `19.0.1.0.0`, license `LGPL-3`).
2. Install it on a fresh disposable DB to confirm the addons path becomes valid and the module loads:
   `docker compose run --rm odoo odoo -d rms_test2 -i retail_management --stop-after-init`.
3. Build only what Milestone A needs: menus/workspace, role groups + server-side guards
   (see `ARCHITECTURE.md` §6.1 gaps), plus tests.

## In-flight / uncommitted work
None — Phase 0 discovery docs are committed with the gate report.

## Blockers and questions for the owner
1. **Gate approval** for Milestone A (Phases 1–4) — see the report in the chat.
2. D-001: dev images come from `mirror.gcr.io` because Docker Hub's CDN blocks this country.
   Production deployment will face the same block (VPN/proxy or approved mirror needed).
3. WSL sees only 3 GB RAM (warning). Odoo works, but installs/tests are slow; 8 GB recommended.
4. Owner: log in as `admin` and change the default password before any shared/network use.

## Decisions pending owner review
- D-001 — use `mirror.gcr.io` for official images in this region (same digests).

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
| 2026-11-01 | OpenCode / deepseek-v4.1-flash-free | Phase 0 discovery complete: dependencies, groups/ACLs, POS offline, extension points; gate report delivered; waiting on owner approval |
| 2026-10-31 | OpenCode / deepseek-v4.1-flash-free | Repo copied to `~/rms`; Docker engine confirmed on Windows, Ubuntu integration off; stopped |
| 2026-10-31 | OpenCode / deepseek-v4.1-flash-free | Stage 0 preflight failed (path + Docker integration); baseline committed |
