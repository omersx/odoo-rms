# Backlog — ideas and proposals for the owner

The agent adds ideas here instead of building them when they would expand scope. The owner decides
what is promoted into the spec or roadmap. The agent must **not** implement backlog items without
approval.

| ID | Date | Idea / proposal | Why it helps | Effort | Risk | Owner decision |
|---|---|---|---|---|---|---|
| B-001 | 2026-11-15 | Narrow the cashier's accounting access: since D-040 he holds Odoo's *Invoicing* right, which is all-or-nothing (`account.move` ACL `1,1,1,1`, rule `[(1,'=',1)]`), so he can also read, create and write **journal entries** (the books) and see every invoice via RPC. No menu shows Accounting to him, but that is cosmetic | Spec §3 gives a cashier no accounting role, and book tampering is the worst thing a shared till login could do. A record rule cannot fix it per-group: rules are OR-ed across a user's groups and the Invoicing rule already allows everything | L | High (needs custom ACLs plus an override of `account.move._post`, which hard-requires the Invoicing group) | Pending |
| B-002 | 2026-11-15 | Show a dashboard to cashiers: the Dashboards app is visible but empty for them — the two existing dashboards are restricted to Invoicing/Administrator | The app the owner asked to keep currently shows "لا توجد لوحة بيانات متاحة"; a simple daily-sales dashboard shared with *Retail Cashier* would make it useful | S / M | Low | Pending |
| B-003 | 2026-11-15 | Split the cashier role in two: a *Retail Cashier* (checkout + customers, no books) and a *Retail Billing* role for whoever invoices from the back office | Lets the shop keep D-039's tight default for most staff and grant D-040's wider rights only to a few, without waiting for the custom-ACL work in B-001 | S | Low | Pending |
