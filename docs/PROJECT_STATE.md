# PROJECT STATE — live handoff file

> **Keep this under ~100 lines and overwrite it; do not append.** History belongs in `git log`,
> `DECISIONS.md` and `DEVELOPMENT_ROADMAP.md`. If it disagrees with the repository or the running system,
> trust reality and fix this file.
> **Visitors and client installs:** this is the template maintainer's working file. To set the app up for a
> company, read `docs/CLIENT_ONBOARDING.md` instead.

**Last updated:** 2026-11-15 · OpenCode · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- **Published:** `https://github.com/omersx/odoo-rms` — public template, branch `main`, tags `phase-1..4-done`
  and `milestone-a`; `.env` and `config/odoo.conf` are ignored and absent from history (D-045).
- Milestone A is implemented and reported (phases 0–4 done). The project is **stopped at the Milestone A
  gate** waiting for the owner's acceptance; Milestone B (POS invoicing, customers/CRM, reports) starts after.

## Current task
Nothing is in flight. The newest work, newest first: the client onboarding runbook for agents (D-047), the
"clone it for a client" proof with a configurable stack identity (D-046), and the publication audit that
purged the owner's wallet data from history (D-045). The repo is a reusable template: all shop-specific data
is database data, no code changes per company.

## Next action (concrete)
**Owner — accept Milestone A.** Run these in the browser at http://localhost:8069 and report anything wrong:
1. Retail Manager: *Retail Management → Point of Sale → Main Register → Open*, sell for cash, check the
   receipt, close the session with the counted cash.
2. Cashier (`cashier` / `cashier`): the app list shows **only Retail Management** (D-041); add a customer;
   invoice a sale with the POS **Invoice** button; open *Retail Management → Invoicing*.
3. Invoice `INV/2026/00005`: one page, wallet block at the bottom. Say if the block is too small on paper
   (`views/report_invoice.xml`, `font-size: 0.9em`).
4. The invoice form's preview pane collapses (D-037) in a window ≥1400 px — still unconfirmed.

Then choose: Milestone B, the production kit (`docs/DEPLOYMENT.md`, written but never executed end to end),
or a real company install following `docs/CLIENT_ONBOARDING.md`.

## In-flight / uncommitted work
None.

## Blockers and questions for the owner
1. **Milestone A gate** — accept the working core or list the changes.
2. **D-001** — Docker Hub's CDN is geo-blocked here; the `.env` uses `mirror.gcr.io` tags. A production
   deployment needs a mirror or VPN first.
3. **WSL has 3 GB RAM** — install + tests take ~8 minutes and PostgreSQL has already recovered once from an
   unclean shutdown. Raise it in `%UserProfile%\.wslconfig` before long runs.
4. **The cashier password is `cashier`** (documented dev default). Change it before a real shop uses this.
5. **The `rms` database still holds Odoo's demo catalogue** (priced in SDG) and the company is still *My
   Company* — a real install replaces both (the onboarding brief asks for them).
6. **B-001 / D-040** — the cashier has Odoo's *Invoicing* right, which is all-or-nothing, so he can reach
   journal entries through a direct request even though no Accounting menu is shown. Accepted by the owner.

## Decisions
`DECISIONS.md` holds D-001…D-047 with alternatives, evidence and a status column (a few say "needs owner
review"). The ones that shape day-to-day work are D-038…D-047: cashier account and rights, app list, Arabic
labels, read-only stock, template hygiene, clone-per-client, onboarding.

## Environment quick facts (full detail: `ARCHITECTURE.md` §2)
- Project `~/rms` in WSL Ubuntu 24.04 · dev URL http://localhost:8069 · `docker compose up -d` · logs `-f odoo`
- Odoo 19.0-20261015 · PostgreSQL 16.15 · Python 3.12.3
- Install: `docker compose run --rm odoo odoo -d <db> -i retail_management --without-demo --stop-after-init`
- Tests (verified, 22 tests / 0 failed):
  `docker compose exec -T odoo sh -c 'odoo -c /etc/odoo/odoo.conf -d rms_test4 -u retail_management --test-enable --stop-after-init --http-port=8799'`
- Dev DB `rms` · disposable `rms_test*` (drop only databases you created). Never add `--test-enable` to the
  `-i` line on a fresh DB: Odoo then runs every core test and hangs.

## Known issues / tech debt
- Docker Hub CDN geo-block (D-001); `scripts/bootstrap.sh` now warns and continues on local images.
- Volumes left by the clone test: `rmsclient_db-data`, `rmsclient_odoo-data` (deleting volumes is a hard stop).
- The production kit (Caddy/HTTPS, `docs/DEPLOYMENT.md`) has never been run end to end.
