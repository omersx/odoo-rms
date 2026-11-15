# Backlog — ideas and proposals for the owner

The agent adds ideas here instead of building them when they would expand scope. The owner decides
what is promoted into the spec or roadmap. The agent must **not** implement backlog items without
approval.

| ID | Date | Idea / proposal | Why it helps | Effort | Risk | Owner decision |
|---|---|---|---|---|---|---|
| B-001 | 2026-11-15 | Narrow the cashier's leftover *reads*: `res.users` records (2 rows) are readable, and `account.move` shows his own POS invoices via POS's `Invoice POS User` rule (2 of 28 on `rms`). Journal entries and other invoices are already denied (D-039) | Spec §3 says a cashier may not view invoice details or customer balances; what is left is small but still data the till does not need | S / M | Med (a `res.users` read rule must not break the avatar/user menu or POS) | Pending |
| B-002 | 2026-11-15 | Show a dashboard to cashiers: the Dashboards app is visible but empty for them — the two existing dashboards are restricted to Invoicing/Administrator | The app the owner asked to keep currently shows "لا توجد لوحة بيانات متاحة"; a simple daily-sales dashboard shared with *Retail Cashier* would make it useful | S / M | Low | Pending |
