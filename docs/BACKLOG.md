# Backlog — ideas and proposals for the owner

The agent adds ideas here instead of building them when they would expand scope. The owner decides
what is promoted into the spec or roadmap. The agent must **not** implement backlog items without
approval.

| ID | Date | Idea / proposal | Why it helps | Effort | Risk | Owner decision |
|---|---|---|---|---|---|---|
| B-001 | 2026-11-15 | Stop a cashier from *reading* invoices and user records (today ACLs from `base.group_user` still allow `account.move` and `res.users` reads, e.g. through the URL `/odoo/customer-invoices`) | Spec §3 says a cashier may not view invoice details or customer balances; menus are hidden but the data is not restricted | M | Med (a record rule on `account.move` for cashiers must not break POS invoicing or session totals) | Pending |
| B-002 | 2026-11-15 | Show a dashboard to cashiers: the Dashboards app is visible but empty for them — the two existing dashboards are restricted to Invoicing/Administrator | The app the owner asked to keep currently shows "لا توجد لوحة بيانات متاحة"; a simple daily-sales dashboard shared with *Retail Cashier* would make it useful | S / M | Low | Pending |
