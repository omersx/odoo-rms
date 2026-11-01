# Decision Log

Append-only. One entry per non-trivial decision, written **when the decision is made**. Tier is from
`AGENTS.md` (1 = decided, 2 = decided and flagged for owner review, 3 = owner decided).
The owner can reverse any Tier 2 entry; mark it `Reversed` and note why.

| ID | Date | Tier | Decision | Alternatives considered | Rationale and evidence | Reversible how | Status |
|---|---|---|---|---|---|---|---|
| D-001 | 2026-11-01 | 2 | Use `mirror.gcr.io/library/*` refs for the Odoo and PostgreSQL images in this dev environment | A) official Docker Hub tags (blocked here); B) VPN/HTTP proxy (owner-controlled); C) build images from source (heavy, unverified) | Docker Hub's blob CDN returns `403 — "The Amazon CloudFront distribution is configured to block access from your country"` for every layer while auth/manifests work. `mirror.gcr.io` serves the same official images: `docker buildx imagetools inspect` gives identical manifest digests (odoo `27f920e0…`, postgres `5db6dac2…`). | Set `ODOO_IMAGE`/`POSTGRES_IMAGE` back to official tags in `.env`; nothing in the repo depends on the mirror | Needs owner review |
| D-002 | 2026-11-01 | 2 | No `pos_hr` in Milestone A: each cashier logs in with their own Odoo user | A) install `pos_hr` for employee-PIN login (adds `hr`, employee records, PIN management); B) own Odoo user per cashier (native `pos.order.user_id` already attributes every order) | Spec §3 requires individual accounts, not shared logins, and attribution already exists natively through the POS user. `pos_hr` adds a second identity layer (employees + PINs) with no requirement behind it; fewer modules = less to configure and test. Owner delegated this choice ("easy and simple"). | Install `pos_hr` later and add `employee_id` usage; no data migration needed | Needs owner review |
| D-003 | 2026-11-01 | 2 | No discount button in Milestone A; no `pos_discount` dependency | A) `pos_discount` fixed-% button (no security file at all — any POS user can discount); B) custom discount workflow (planned extension) | `pos_discount` has **no group restriction** (`find … -path '*security*'` returns nothing), which conflicts with "exceptional discounts need authorization". Milestone A does not require discounts; price edits stay restricted to managers (`pos.config.restrict_price_control`, server-side guard in Phase 2). | Install `pos_discount` or add a guarded discount later (extension) | Needs owner review |
| D-004 | 2026-11-01 | 2 | Customers are created/edited by Administrators only (native behaviour, `base.group_partner_manager`); cashiers may search and select existing customers in POS | A) grant `base.group_partner_manager` to cashiers; B) custom cashier-limited partner form | Spec permission matrix says "Create/edit customers: Only if enabled, approved fields only" — that is a custom form + record rules, i.e. extra code for no Milestone A requirement. Native POS already lets a cashier attach an existing customer to an order. | Give cashiers `base.group_partner_manager` (crude, full create/edit) or build the guarded form later | Needs owner review |
| D-005 | 2026-11-01 | 2 | Retail Management menus point at native actions with native groups on each item; no custom menus duplicating native screens | A) build custom list/form views; B) copy native menus by XML id remapping | Every item maps to a verified native action (`point_of_sale.action_pos_config_kanban`, `stock.product_template_action_product`, `stock.action_view_quants`, `account.action_move_out_invoice`, `contacts.action_contacts`, `point_of_sale.action_pos_configuration`). Visibility verified per group on `rms_test2`: cashiers see Point of Sale + Products only. Hiding is not security — ACLs still govern. | Edit `views/retail_menu.xml`; nothing depends on the menu ids | Needs owner review |

**Status values:** `Accepted` · `Needs owner review` · `Reversed` · `Superseded by D-xxx`

## Entry template (copy into the table, or use a section below for long entries)
- **Decision:** what was decided, in one sentence.
- **Context:** the problem or ambiguity.
- **Options:** A, B, C with one-line pros/cons.
- **Choice and why:** include evidence (file path in the Odoo 19 source, test result, command output).
- **Consequences / how to reverse.**
