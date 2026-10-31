# Retail Management System (RMS) — Product Specification

**Platform:** Odoo 19 Community Edition
**Audience:** Product owner, Odoo developer, AI coding agents (OpenCode)
**Status:** Product requirements. Every technical detail (model names, groups, module dependencies,
POS behaviour) must be verified against the exact Odoo 19 build before implementation.

This document defines **what** to build. Technical design is in `ARCHITECTURE.md`; progress is in
`DEVELOPMENT_ROADMAP.md`; agent rules are in `AGENTS.md`.

---

## 1. Purpose and principles

Build a simple, reliable, general-purpose retail system on Odoo 19 Community that suits small and
medium retailers (general stores, supermarkets, clothing/footwear, electronics, stationery/books,
mixed merchandise) **through configuration, not separate hard-coded applications**.

A retailer should be able to: maintain products → receive and track stock → sell at a POS → record
payments and sessions → invoice customers → manage simple customer records → review basic reports,
with a small set of roles. It must feel like one coherent **Retail Management** app on top of
standard Odoo.

Principles:
- **Simple first.** Common daily tasks; no ERP clutter for cashiers.
- **Reuse Odoo.** Native POS, stock, accounting and Contacts. Not a full ERP.
- **Extend, never fork.** Never modify Odoo core; isolate custom code in add-ons.
- **Configurable.** Barcode use, variants, lots/expiry, serials and locations are options.
- **Traceable.** Sales, payments, invoices and stock movements stay linked and consistent.
- **Safe by default.** Cashiers never get admin rights implicitly.
- **Honest about offline.** Only native Odoo POS offline behaviour, accurately documented.
- **Upgrade-friendly.** Small, documented customizations.

---

## 2. Scope

Delivery is split into three **milestones**. The agent stops for owner approval between them.

### 2.1 Milestone A — Working core (sell and track stock)
- Retail Management menu/workspace.
- Administrator and Cashier roles, enforced server-side.
- Products, categories, barcodes, prices, units; stock receipt, adjustment, movement history.
- Native POS: sessions, checkout, cash payment, receipts, refunds via native workflow, multiple cashiers.

### 2.2 Milestone B — Complete MVP
- Customer invoicing from POS and backend using standard accounting.
- Simple customer management (retail CRM) on native Contacts.
- Simple dashboard and basic reports (see §5).

### 2.3 Milestone C — Release readiness
- Offline testing and documented limitations, backup/restore test, upgrade test, hardware tests
  (printer, barcode scanner), user guides, owner acceptance.

### 2.4 Planned extensions (not MVP; owner approval required)
Supplier purchasing and bills · advanced stocktaking sessions · multiple stores/warehouses ·
product import/export · cash in/out and discrepancy workflows · **custom** refund/discount approval
workflows (native POS restrictions are in scope) · low-stock **alerts/notifications** (a low-stock
*view* is in scope) · business-profile presets · inventory-only deployment profile (subject to
verified module dependencies) · multiple POS terminals beyond the first setup.

### 2.5 Out of scope
Manufacturing/MRP · payroll/HR · leads, opportunities, sales pipelines, marketing automation,
loyalty/rewards, automated customer messaging · e-commerce · custom accounting engine · custom POS
engine or custom offline sync engine · multi-company/SaaS tenancy · industry-regulated workflows
(e.g. pharmacy) · native mobile app.

---

## 3. Roles and permissions

Odoo users, security groups and POS employee access are **not the same thing**. The agent must map
the two roles below onto the real Odoo 19 mechanisms and test the mapping.

**Administrator** — owner or trusted manager. Manages products, stock, POS configuration, invoices,
customers, reports and users; may also use POS; approves refunds, exceptional discounts and price
overrides. *Decision:* Administrator must **not** automatically mean Odoo's technical/superuser
settings access. Separate day-to-day retail administration from Odoo system administration where
the build allows it; record the chosen group mapping in `ARCHITECTURE.md`.

**Cashier** — checkout only. Individual account per person; no shared logins.

### Permission matrix (initial proposal — verify and test)
| Function | Administrator | Cashier |
|---|---|---|
| Use POS | Yes | Yes |
| Open/close POS session | Yes | Configurable |
| View own POS orders | Yes | Yes |
| View all POS orders | Yes | No by default |
| Create/edit products | Yes | No |
| View product info in POS | Yes | Yes |
| Receive stock / adjust stock | Yes | No |
| View stock quantities | Yes | Limited/optional |
| Search/select customers (POS) | Yes | Yes |
| Create/edit customers | Yes | Only if enabled; approved fields only |
| Manage customer tags/groups | Yes | No |
| View purchase history and basic insights | Yes | Limited, if enabled |
| View customer balance / invoice details | Yes | No |
| Create invoice from POS | Yes | Only if enabled |
| Manage invoices / accounting | Yes | No |
| Approve refunds | Yes | No by default |
| Normal discount | Yes | Limited by policy |
| Exceptional discount / price override | Yes | No by default |
| View reports | All | Own/limited, if needed |
| Manage users / settings | Yes | No |

Hidden menus are not security. Access must be enforced at model and server level and tested through
direct RPC/ORM calls as well as the UI.

---

## 4. User experience

One entry point named **Retail Management**, opening a simplified workspace. Suggested menu:
Dashboard · Point of Sale · Products · Inventory · Invoicing · Customers · Reports · Settings
(Administrator only). Cashiers should work in the POS register and never need backend
inventory/accounting menus.

- **POS:** use native Odoo 19 POS; customize only for a clear usability need. Flow: sign in → open
  or join session → search/scan → adjust cart → select customer if needed → pay → receipt → next order.
- **Inventory screens:** product list/form, stock by product/location, receive stock, adjustment/count
  (authorized only), movement history, low-stock view. Always use standard stock operations.
- **Invoicing:** list with status filters, create, print/send, register payment (authorized only),
  link back to the source POS order. A POS receipt is not a legal invoice; follow local rules.
- **Customers:** searchable list and a profile showing contact details, tags, order count, total
  purchases, last purchase date, recent POS orders and invoices (links to native records), internal
  notes, and outstanding balance **only** for users with financial permission. Cashier-facing
  screens expose only what checkout needs.
- **Dashboard (Milestone B):** today's sales and order count, session status, low-stock items,
  recent sales, unpaid/overdue invoice summary (admin only), quick actions. Values are computed from
  real records; never store duplicate totals.

---

## 5. Functional requirements

Milestone column: **A**, **B**, **C**, or **Ext** (planned extension).

### 5.1 Products
| ID | Requirement | M |
|---|---|---|
| PROD-01 | Administrator can create, edit, archive and search products. | A |
| PROD-02 | Product has name, internal reference, barcode, category, image, sales price, cost, unit of measure, type (as supported). | A |
| PROD-03 | Product can be made available in POS. | A |
| PROD-04 | Product categories can be maintained. | A |
| PROD-05 | Variants are optional; never forced on simple products. | Ext |
| PROD-06 | Lot/expiry/serial tracking, if enabled, uses standard Odoo tracking. | Ext |
| PROD-07 | Cashiers cannot edit master product data. | A |

### 5.2 POS and sales
| ID | Requirement | M |
|---|---|---|
| POS-01 | Authorized users can open and operate a POS session. | A |
| POS-02 | More than one cashier can work concurrently per native session/employee configuration. | A |
| POS-03 | Each transaction is attributable to the correct user/employee and POS. | A |
| POS-04 | Find products by name, reference or barcode where supported. | A |
| POS-05 | Adjust quantity and permitted discounts before validation. | A |
| POS-06 | Support configured payment methods (cash at minimum). | A |
| POS-07 | Validated orders are stored and never silently overwritten. | A |
| POS-08 | Receipt available after validation. | A |
| POS-09 | Customer optional for cash sales; required when the invoice workflow needs it. | B |
| POS-10 | Refunds/returns follow native Odoo workflow and permissions. | A |
| POS-11 | Session open/close controls retained. | A |
| POS-12 | Cash differences and session totals reviewable by authorized users. | A |

### 5.3 Inventory
| ID | Requirement | M |
|---|---|---|
| STK-01 | Administrator can view stock quantities. | A |
| STK-02 | Completed POS sales update stock through native POS/stock integration. | A |
| STK-03 | Receive stock via standard receipts/pickings. | A |
| STK-04 | Adjustments require permission and, where supported, a reason. | A |
| STK-05 | Stock movements stay traceable. | A |
| STK-06 | Computed stock quantities are never overwritten directly. | A |
| STK-07 | Negative-stock behaviour is explicitly decided and tested (do not assume it is blocked). | A |
| STK-08 | Single store/warehouse first; multi-store deferred. | Ext |
| STK-09 | Basic physical count/inventory adjustment via standard workflow. | A |
| STK-10 | Low-stock **view** from minimum quantities/reordering rules where supported. | B |
| STK-11 | Internal transfers use standard picking/move workflows. | Ext |
| STK-12 | Lot/serial information is preserved where tracking is enabled. | Ext |

### 5.4 Invoicing
| ID | Requirement | M |
|---|---|---|
| INV-01 | Authorized users create customer invoices with standard accounting. | B |
| INV-02 | POS orders can generate invoices through the supported workflow. | B |
| INV-03 | Totals, taxes, currency and rounding follow Odoo configuration. | B |
| INV-04 | Invoices printed/sent with standard methods. | B |
| INV-05 | Payments registered through configured journals. | B |
| INV-06 | Invoice status reflects the real accounting state. | B |
| INV-07 | Cashiers cannot post, cancel or modify invoices beyond granted permissions. | B |

### 5.5 Customers (simple retail CRM)
| ID | Requirement | M |
|---|---|---|
| CUST-01 | Create, view, update, archive and search customers using native Contacts. | B |
| CUST-02 | Basic details: name, phone, email, address. | B |
| CUST-03 | Groups/tags, preferably native partner categories. | B |
| CUST-04 | Profile shows linked POS purchase history and invoices from native records; no duplicate history stored. | B |
| CUST-05 | Internal notes, without exposing sensitive notes to unauthorized users. | B |
| CUST-06 | Insights: order count, total purchases, last purchase date. Rules for refunds, cancelled orders, taxes and currency must be defined and tested. | B |
| CUST-07 | Outstanding balance and invoice financial details only for users with accounting permission. | B |
| CUST-08 | Cashiers can search/select customers; creation/editing is configurable and limited to approved fields. | B |
| CUST-09 | Customer and financial permissions enforced server-side. | B |
| CUST-10 | No parallel customer database; no duplicated orders, invoices or payments. | B |
| CUST-11 | Leads, pipelines, marketing automation, loyalty and messaging excluded. | — |

### 5.6 Configuration
| ID | Requirement | M |
|---|---|---|
| CFG-01 | Administrator configures business identity and contact details. | A |
| CFG-02 | Currency, taxes, fiscal settings per local requirements. | B |
| CFG-03 | POS payment methods and receipt details. | A |
| CFG-04 | Optional features (barcode, tracking) via clear settings where appropriate. | A |
| CFG-05 | Ordinary configuration needs no code edits. | A |

### 5.7 Reporting (Milestone B)
| ID | Requirement |
|---|---|
| REP-01 | Sales by date range. |
| REP-02 | Sales by product and category. |
| REP-03 | Sales by POS/cashier where source data supports it. |
| REP-04 | Current stock and low-stock products. |
| REP-05 | Invoice status and totals. |
| REP-06 | Reports use source records and respect access rights. |
| REP-07 | POS session summaries and payment-method totals. |
| REP-08 | Stock movement/valuation review where the configured Community modules support it. |

### 5.8 Purchasing (planned extension — Ext)
Supplier contacts, purchase orders, receipts, supplier bills, all via standard Odoo records with
cashiers excluded by default. Verify Community availability before committing. Not part of the MVP.

---

## 6. Offline POS

Odoo 19 POS has native, **limited** offline behaviour. Use it as the baseline and document it; do not
build a sync engine. Per Odoo's documentation (verify on the build): orders made offline are stored in
the browser and synchronized on reconnect; invoicing requested offline is generated afterwards;
real-time stock sync between disconnected terminals is unavailable; several backend-dependent
functions are unavailable.

Rules: never promise whole-ERP offline operation or real-time shared stock; indicate online/offline
status if the native UI does; train cashiers not to close/reload the browser or clear its cache while
unsynchronized orders exist.

Offline acceptance tests (Milestone C, on the exact build):
1. Open a session online and let products load.
2. Disconnect; complete a cash sale from cached products.
3. Confirm the order persists in the browser; reconnect.
4. Confirm it synchronizes **exactly once**, with correct backend order, payment and stock effects.
5. Repeat with several offline orders.
6. Test refresh/closure only in a controlled environment; document data-loss risk.
7. Test an invoice request made offline and confirm deferred behaviour.
8. Test two terminals offline simultaneously; document that they cannot see each other's changes.

Do not mark unsupported offline features as passed.

---

## 7. Multi-cashier and sessions

Use native POS sessions and employee/user mechanisms. Enable multi-employee login only if the store
workflow needs it. One individual identity per person; never share an administrator login. Associate
every order with cashier and POS. Use a dedicated cash payment method/journal per POS where
appropriate. Close sessions per the store's shift procedure and review expected vs counted cash.
Inspect native behaviour before proposing custom code.

---

## 8. Data ownership

Standard Odoo records are the single source of truth. Concepts below map to native records; exact
model names must be verified.

| Concept | Source of truth |
|---|---|
| Product, variant, category | Native product records |
| Stock on hand, receipts, adjustments | Native stock quant/move/picking workflows |
| POS sale, session, payment | Native POS order/session/payment |
| Customer, supplier | Native Contacts |
| Invoice, journal | Native accounting records |
| Access | Users, groups, ACLs, record rules |

Data integrity rules: no manual changes to computed stock; no duplicate invoice for one sale; no
order marked paid without a valid payment; cashiers cannot edit validated orders; preserve links
between order, session, payment, invoice and stock movement; ORM over raw SQL.

---

## 9. Security and reliability

Enforce on the server with groups, ACLs, and (only when needed) record rules. Least privilege for
cashiers. Restrict stock adjustments, refunds, price overrides, invoice posting and configuration.
Keep individual identities. Use Odoo chatter/logging where suitable; do not claim full auditing
without tests proving it. Never log passwords, tokens or unnecessary personal data. Production:
HTTPS, restricted DB/server access, backups with a tested restore, documented upgrades.

---

## 10. Configuration and profiles

Adapt to different retailers through settings: business identity, currency/timezone, taxes, units,
barcode use, payment methods, receipt/invoice layout, discount permissions, optional lot/serial
tracking, warehouse/location. Business-profile presets (supermarket, clothing, electronics, etc.) are
an **extension**: they may only pre-set standard features, must stay transparent and editable, must
not make hidden changes, and must never claim regulatory compliance. A retailer-specific extension
module must be addable without changing the generic core.

---

## 11. Acceptance scenarios

| # | Scenario | Milestone |
|---|---|---|
| A | **Product setup:** admin creates product (name, price, category, barcode); it appears in POS after refresh; cashier finds it but cannot edit master data. | A |
| B | **Standard sale:** cashier opens session, adds two products, changes a quantity, pays cash, validates; receipt produced; order visible in backend; stock updated per native POS stock workflow. | A |
| D | **Receive stock:** admin receives and validates a receipt; quantity rises correctly; movement history shows it. | A |
| E | **Permissions:** cashier denied product edit, stock adjustment, tax/settings change (via UI **and** direct RPC); allowed sale succeeds; admin can manage and use POS. | A |
| F | **Multiple cashiers:** two cashiers work concurrently; correct attribution; nothing duplicated or lost; session/payment totals consistent. | A |
| H | **Refund and close:** authorized refund through native workflow; original transaction traceable; session close totals correct; cash discrepancy behaviour tested. | A |
| C | **Invoice:** customer assigned; invoice requested via POS; generated and linked; printable; payment registered; status matches accounting state. | B |
| I | **Customer:** profile shows tags, order count, total purchases, last purchase, linked orders/invoices; refunds/cancellations handled per defined rules; cashier cannot see balance or invoice details (UI and RPC); no duplicate customer/transaction data. | B |
| J | **Reports:** report figures reconcile with source records and respect access rights. | B |
| G | **Offline:** run §6 tests; record all native limitations. | C |

---

## 12. Quality requirements and definition of done

Quality: no critical permission bypass; no duplicate order/invoice in tested retry scenarios; no
unexplained stock changes; no unhandled server errors in core workflows; usable on intended POS
screen sizes; clear validation messages; automated tests for custom models, security and logic; a
manual checklist for hardware and offline behaviour.

**Milestone A done** when scenarios A, B, D, E, F, H pass, the module installs/upgrades cleanly, and
no critical security issue is known.
**Milestone B done** when scenarios C, I, J pass and customer/financial permissions are verified
server-side.
**Release (Milestone C) done** when additionally: offline behaviour is tested and limitations
documented; backup/restore and upgrade are tested; hardware is tested; setup, cashier, administrator
and deployment guides exist; known issues are recorded and accepted by the owner.

---

## 13. Decisions and open questions

Confirm during discovery or before production; use standard Odoo defaults where safe.

| Topic | Initial recommendation | Confirm |
|---|---|---|
| Store structure | One company, one store, one warehouse | Before deployment |
| Cashiers | Individual accounts; no shared logins | Before user setup |
| Admin POS access | Administrator can also sell | Initial setup |
| Administrator ≠ technical superuser | Separate where the build allows | Phase 2 |
| Cashier refunds | Restricted; admin approval by default | Before training |
| Discounts | Normal limited; exceptional needs admin | Before POS rollout |
| Negative stock | Decide explicitly (STK-07) | Phase 3 |
| Payment methods | Cash first | Before deployment |
| Taxes / currency | Per retailer's country and operating currency | Before real invoicing |
| Cashier customer creation | Off by default; owner decides | Phase 6 |
| Customer insight rules | Define refund/cancel/tax/currency treatment | Phase 6 |
| Offline | Native only | Before acceptance |

**Compliance note:** invoice numbering, tax calculation, mandatory invoice fields, fiscal devices and
e-invoicing vary by jurisdiction. Have a qualified local adviser review before real transactions.

---

## 14. Official references

Use Odoo 19 documentation and the exact Odoo 19 Community source only; never silently substitute
Odoo 18, 17 or master.
- https://www.odoo.com/documentation/19.0/
- https://www.odoo.com/documentation/19.0/developer.html
- https://www.odoo.com/documentation/19.0/applications/sales/point_of_sale.html
- https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory.html
- https://www.odoo.com/documentation/19.0/applications/finance/accounting/customer_invoices.html
- https://github.com/odoo/odoo

If a link has moved, find the matching 19.0 page on the official site.
