# Changelog

One section per release tag. The version is the module version (`__manifest__.py`); the tag is `v` + it.

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
