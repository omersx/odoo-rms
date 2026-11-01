# RMS Development Roadmap

**Platform:** Odoo 19 Community Edition
**Current status:** Phase 0 not started

Scope and requirement IDs are in `RETAIL_MANAGEMENT_SPEC.md`; technical facts in `ARCHITECTURE.md`.

## How to use this roadmap
Legend: `[ ]` not started · `[-]` in progress · `[x]` done **and verified** · `[!]` blocked / needs decision.
Do not tick a box because code was generated. Record the test or evidence in the progress log.

**Approval gates (default autonomy level 2):** the agent works through phases within a milestone on its
own, but stops and reports at the end of **Phase 0** and at the end of **each milestone**, then waits for
owner approval. The owner can change the level in `PROJECT_STATE.md` (1 = stop every phase, 3 = report
and continue); hard stops in `AGENTS.md` apply at every level.

---

# MILESTONE A — Working core

## Phase 0 — Discovery  *(gate: owner approval required)*
- [x] Stage 0: preflight 0 failures (2026-11-01); `docker compose up -d` serves HTTP 200; facts recorded in `ARCHITECTURE.md` §2; kit fixed (`--without-demo`) and geo-block documented.
- [ ] Inspect repo, branch, Git status, existing code and conventions.
- [ ] Identify Odoo 19 version/revision, PostgreSQL version, config, addons paths, run/test commands.
- [ ] Inspect available standard modules and manifests; record dependency graph.
- [ ] Verify security groups, POS employee/cashier access, POS extension APIs.
- [ ] Verify native POS offline capability on paper (testing happens in Phase 8).
- [ ] Inspect OpenCode setup and any installed tools; do not duplicate or assume integration.
- [ ] Fill `ARCHITECTURE.md` §2, §4, §6.1; list what needs configuration vs custom code.
- [x] Owner chooses the dev runtime: Docker Desktop, WSL integration enabled 2026-11-01; environment checklist in `WINDOWS_SETUP.md` §5 passes except disposable DB/test command (Phase 1).
- [ ] Review the Docker kit (compose files, configs, scripts) against the real Odoo 19 image; record fixes.
- [ ] Owner confirms scope and open decisions.

**Exit:** versions and dependencies verified; blockers and open questions documented.

## Phase 1 — Minimal custom module
- [ ] Create `retail_management` with a manifest containing only verified, required dependencies.
- [ ] Add the Retail Management menu/workspace linking to standard Odoo actions.
- [ ] Clean install and upgrade on a disposable database; note uninstall implications.

- [ ] *(Optional)* Trial an external static review tool on `retail_management` per `OPTIONAL_TOOLS.md` §2; record the decision.

**Exit:** clean install/upgrade; no duplicated Odoo logic; no server errors.

## Phase 2 — Roles and security
- [ ] Map Administrator and Cashier to verified groups/POS access; decide the Administrator vs
      technical-superuser separation.
- [ ] Complete the permission matrix (spec §3) against real groups.
- [ ] Restrict sensitive operations server-side.
- [ ] Automated tests for allowed **and** denied operations (UI and direct RPC/ORM).

**Exit:** cashier cannot bypass restrictions; administrator can manage and use POS.

## Phase 3 — Products and inventory
- [ ] Product catalog: categories, price, cost, unit, barcode, internal reference.
- [ ] Product search and barcode use.
- [ ] Stock overview and movement history.
- [ ] Receive stock; authorized stock adjustment; basic count/adjustment.
- [ ] Decide and test negative-stock behaviour (STK-07).
- [ ] Tests for any custom inventory logic.

**Exit:** scenarios A and D pass; quantities reconcile with native records.

## Phase 4 — POS
- [ ] Configure POS and payment methods (cash first); cashier access and attribution.
- [ ] Open/close session; search, cart, barcode scan; cash payment; receipt.
- [ ] Refunds/returns with permission restrictions.
- [ ] Concurrent cashiers; session closing totals; cash difference behaviour.
- [ ] Verify POS-to-stock behaviour.
- [ ] POS frontend customization only for approved needs.

**Exit:** scenarios B, E, F, H pass without breaking native POS behaviour.

### ▶ MILESTONE A GATE — report and wait for owner approval

---

# MILESTONE B — Complete MVP

## Phase 5 — Invoicing
- [ ] Verify required accounting modules in this Community build.
- [ ] Configure invoicing workflow; invoice from POS (customer required).
- [ ] Posting, payment registration, status; printing/sending with standard features.
- [ ] Tax/accounting configuration reviewed by a qualified local adviser.

**Exit:** scenario C passes; invoices and payments reconcile with source transactions.

## Phase 6 — Simple customer management (retail CRM)
- [ ] Confirm native partner model and POS/invoice relations on this build.
- [ ] Customer list/profile on native Contacts; tags via native categories.
- [ ] Purchase history and invoices shown from source records (no duplication).
- [ ] Internal notes (native feature or minimal access-controlled extension).
- [ ] Insights (order count, total purchases, last purchase) with documented refund/cancel/tax/currency rules.
- [ ] Outstanding balance visible to authorized users only.
- [ ] Cashier permissions for search/select/create/edit/financial visibility, enforced server-side.
- [ ] Tests: links, history accuracy, access control, sensitive-data exposure.

**Exit:** scenario I passes; no duplicate customer/order/invoice data; restrictions verified via RPC.

## Phase 7 — Dashboard and reports
- [ ] Dashboard: today's sales/orders, session status, low-stock, recent sales, unpaid invoices (admin).
- [ ] Reports: sales by period/product/category/cashier; stock and low-stock; invoice status; session/payment totals.
- [ ] Permission-aware; reconciled against source records; tested with representative data volumes.

**Exit:** scenario J passes.

### ▶ MILESTONE B GATE — report and wait for owner approval

---

# MILESTONE C — Release readiness

## Phase 8 — Offline, deployment, release
- [ ] Run the offline acceptance tests (spec §6); document limits and cashier recovery steps.
- [ ] Backup and restore test; upgrade test on a staging copy.
- [ ] Barcode scanner, printer, and screen-size tests on target hardware.
- [ ] Production configuration and HTTPS using the deployment kit (`DEPLOYMENT.md` §4–5, §9 checklist).
- [ ] Verify the kit end to end: first run, `setup.sh prod`, database creation, backup, restore into a new DB, update/rollback.
- [ ] Administrator, cashier and deployment guides.
- [ ] Known-issues list; owner acceptance.

**Exit:** release checklist passes; remaining limitations accepted by the owner (scenario G).

---

# Planned extensions — not committed, owner approval required
- [ ] Supplier purchasing and bills
- [ ] Advanced stocktaking and discrepancy approval
- [ ] Multiple stores/warehouses and transfers
- [ ] Variants, lots/serials, import/export
- [ ] Cash in/out and discrepancy workflows
- [ ] Custom refund/discount approval workflows; low-stock alerts
- [ ] Business-profile presets; inventory-only profile (dependency validation first)

---

## Progress log
| Date | Phase / task | Status | Evidence / test | Next action |
|---|---|---|---|---|
| | Roadmap created | Not started | — | Run `INITIAL_PROMPT.md` (Phase 0) |
| 2026-10-31 | Phase 0 / Stage 0 | Blocked | `scripts/preflight.sh` in WSL Ubuntu 24.04: 2 FAIL — (1) project under `/mnt/c/...`; (2) Docker daemon unreachable from Ubuntu, no `/var/run/docker.sock`, Docker Desktop WSL integration off. 1 WARN — 3 GB RAM. Docker CLI 29.8.0 / Compose 5.5.1 present. Stack never started; kit unverified. | Owner: move project to `~/rms`, enable Docker Desktop WSL integration for Ubuntu, re-run `scripts/preflight.sh` then `scripts/bootstrap.sh dev` |
| 2026-10-31 | Phase 0 / Stage 0 | Blocked (narrowed) | Repo copied to `~/rms`, `git status` clean, 30 tracked files. Docker engine 29.8.0 answers on Windows; from Ubuntu still no socket after `wsl --terminate Ubuntu`; `EnableIntegrationWithDefaultWslDistro=false`. | Owner: enable WSL integration for Ubuntu in Docker Desktop, Apply & restart; then agent runs preflight + bootstrap |
| 2026-11-01 | Phase 0 / Stage 0 | Done | Preflight 0 failures. Docker Hub CDN geo-blocked (CloudFront 403); images pulled from `mirror.gcr.io` with identical digests (D-001). Odoo `19.0-20261015`, PostgreSQL 16.15, Python 3.12.3. `rms` DB created (base, no demo); `http://localhost:8069/web/login` HTTP 200. `--without-demo=all` fixed to `--without-demo`. | Phase 0 discovery: module manifests, groups, POS offline, extension points |

## Maintenance rules
1. Update status only after checking the real repository and test results.
2. Record blockers and decisions instead of silently skipping tasks.
3. Do not expand scope without recording owner approval.
4. At each phase end summarize changed modules, tests, evidence and remaining risks.
5. The roadmap holds phase status; `PROJECT_STATE.md` holds the live pointer (current task, next action,
   blockers). Do not copy the checklist into the state file.
6. Approval gates follow the autonomy level in `PROJECT_STATE.md` (default: stop after Phase 0 and at each
   milestone gate; hard stops in `AGENTS.md` always apply).
