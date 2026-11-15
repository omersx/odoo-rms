# Changelog

One section per release tag. The version is the module version (`__manifest__.py`); the tag is `v` + it.

## [19.0.1.19.0] — 2026-11-15

Documentation, CI and client-onboarding release. **No business logic changed**; the module version is bumped
so a shop can tell the two builds apart and upgrade through the normal staged path (`docs/RELEASES.md`).
Verified on **Odoo 19.0-20261015 / PostgreSQL 16**: 22 tests, 0 failed, and green CI on every commit below.

- `AGENTS.md` starts with a **mode check**: if `CLIENT_NOTE.md` exists, an agent follows only
  `docs/CLIENT_ONBOARDING.md`, edits nothing under `custom_addons/` or `docs/`, and does not commit. Hard
  stops and technical invariants still apply.
- CI: `.github/workflows/tests.yml` installs the module on a throwaway database and gates on
  `0 failed, 0 error(s) of N tests` on every push and pull request; runner pinned to `ubuntu-24.04`,
  `actions/checkout@v7`; badge in the README.
- Releases: `docs/RELEASES.md` (a shop runs a tag, staged update, rollback via backup) and this changelog.
  The tag equals the module version, and a tag is only cut on a commit with green CI.
- Onboarding checks out the **newest release tag** instead of a hard-coded one; the client brief is written
  inside the client clone, not in the template checkout.
- README and roadmap now state what is actually built: reports and the customer dashboard are **not built**
  (`B-002`); development is paused after Milestone A.

## [19.0.1.18.0] — 2026-11-15

First published release of the template. Verified on **Odoo 19.0-20261015 / PostgreSQL 16** with a clean
install on a fresh database (no demo data): **22 tests, 0 failed**.

- Two roles mapped onto native Odoo groups: Retail Cashier, Retail Manager (neither is Odoo's technical
  administrator).
- Server-side guards: refunds and stock validation are manager-only, also through RPC and POS sync.
- One **Retail Management** app for the shop's five screens; native Odoo apps stay with the administrator.
- Full-page icon launcher that re-reads menus when it opens; PWA install with its own icon.
- Arabic labels (`i18n/ar_001.po`) with English source; RTL supported by Odoo.
- Cashier can read on-hand quantities in a read-only list; product, stock and settings changes stay with
  the manager.
- POS: payment methods in two columns, 256 px icons, receipt prints the QR only, camera Scan button on the
  product barcode field.
- Invoices: one page, `طرق الدفع` payment block fed by the company's bank accounts, wallet wording and the
  document footer are company data, the customer portal shows the posted invoice itself.
- Docker kit: dev and prod overlays, generated secrets, configurable project/database/port, backup and
  restore scripts, Caddy + HTTPS kit (written, not yet executed end to end).
- Client onboarding as data entry: `docs/CLIENT_ONBOARDING.md`; releases and updates in
  `docs/RELEASES.md`.
