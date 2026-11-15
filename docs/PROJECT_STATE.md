# PROJECT STATE — release card

> Overwrite this file; keep it under ~30 lines. History is in `git log`, decisions in `DECISIONS.md`,
> verified technical facts in `ARCHITECTURE.md`. If it disagrees with reality, fix this file.
> **Visitors / client installs:** read `docs/CLIENT_ONBOARDING.md`. To change code: `AGENTS.md`.

**Last updated:** 2026-11-15 · **autonomy:** 2   <!-- owner edits: 1 guided, 2 standard, 3 high -->

## Status: released template, development finished
- `https://github.com/omersx/odoo-rms` — public, branch `main`, tags `phase-1..4-done` and `milestone-a`.
- `retail_management 19.0.1.19.0` on Odoo 19.0 / PostgreSQL 16; a clean install on a fresh database passes
  **22 tests, 0 failed**. CI (`.github/workflows/tests.yml`) runs the same install + tests on every push.
- Shops run a **release tag** (`v19.0.1.19.0`, the newest), never `main` — `docs/RELEASES.md`.
- Owner's position (2026-11-15): the app is ready, no further development requested. A new company is
  onboarded with **data only** (`docs/CLIENT_ONBOARDING.md`) — no code changes, no local commits.

## Open items (none blocking)
1. The production kit (Caddy/HTTPS, `docs/DEPLOYMENT.md`) has never been run end to end.
2. The invoice printout (one page, wallet block) and the collapsible preview pane (D-037, ≥1400 px) were never
   confirmed in a browser by the owner.
3. B-001: the cashier holds Odoo's *Invoicing* right, so journal entries are reachable through a direct
   request. Accepted trade-off, tracked in `BACKLOG.md`.
4. The development database `rms` still holds Odoo's demo catalogue and *My Company* — not a shippable install.
5. Dev credentials `admin` / `cashier` (`cashier`) must be changed in any real shop.

## Environment (commands: `AGENTS.md` § Running it)
`~/rms` in WSL Ubuntu · http://localhost:8069 · DB `rms` · tests on `rms_test4` · Odoo 19.0-20261015.
