# Client onboarding — set up this template for one company

**Who this is for:** a human, or an AI coding agent (opencode, Claude Code, …), installing RMS for a new
company from a fresh clone of `https://github.com/omersx/odoo-rms`.

**This is data entry against a running Odoo, not software development.** No company needs a change in
`custom_addons/`. With no local commits the clone stays updatable — but **deliberately**: install a pinned
release tag and never `git pull` a live shop's checkout (see `docs/RELEASES.md`).

## 0. Do not follow the development notes

`docs/PROJECT_STATE.md`, `docs/HANDOFF_PROMPT.md` and the autonomy tiers in `AGENTS.md` exist for
**developing the template**. On a client install their "next action" belongs to the template's own
history, not to your job. This file replaces them.

## 1. Get the brief (the only thing to ask the owner)

Write the answers into `CLIENT_NOTE.md` **inside the client clone from step 2** — not in the template
checkout, where it would be a stray ignored file. Asking the owner happens first; the file is written once the
clone exists. Ask for the items marked ● and skip the rest if the owner has none.

| Item | Detail | Ends up in |
|---|---|---|
| ● Company | trade name, address, phone (this is the number printed on invoices), country, currency | Settings → Companies |
| ● Logo | PNG or SVG, ideally square | same, *Logo* field |
| ● Wallets | for each: bank name, account number, account-holder name. Plus the two wordings if the defaults do not fit: title (default `طرق الدفع`) and note (default `ارسل اشعار الدفع في الرقم واتساب`) | same, *Invoices* tab: one **bank account per wallet** + `Payment block title` / `Payment note` |
| ● Products | name, sale price, cost, barcode, unit, category, tax per product | Retail Management → Products |
| ● Tax | the rate(s), and one decision: do prices include tax? | Settings → Taxes, Invoicing → Configuration → Taxes |
| ● Register | register name, payment methods (cash / card / wallet names), receipt footer text | Retail Management → Settings |
| ● Users | manager (name + email), cashier (name + email), language for each | Settings → Users |
| ○ Opening stock | product + quantity on hand | Inventory → Physical Inventory (as admin) |

Never collect passwords from another system, and never write any of this into a tracked file.

## 2. Install (WSL2/Ubuntu; Windows prerequisites in `docs/WINDOWS_SETUP.md`)

Docker Desktop with WSL integration must already be running — installing Docker/WSL is a human step, not
something an agent can do.

```bash
git clone https://github.com/omersx/odoo-rms.git ~/rms-<client>
cd ~/rms-<client>
git checkout "$(git tag --list 'v[0-9]*' --sort=-v:refname | head -1)"   # newest release, never main (docs/RELEASES.md)
scripts/setup.sh dev          # generates .env + config/odoo.conf with random secrets
```

Edit three lines in `.env` so this shop cannot collide with another stack on the same machine:

```
COMPOSE_PROJECT_NAME=rms<client>
DB_NAME=rms<client>
ODOO_PORT=8071                # any free port
```

```bash
scripts/bootstrap.sh dev      # preflight → database → Odoo up; must end with HTTP 200 and 6/6
set -a; source .env; set +a
docker compose run --rm odoo odoo -d "$DB_NAME" -i retail_management --without-demo --stop-after-init
docker compose up -d odoo
```

Open `http://localhost:<ODOO_PORT>`. Log in as **`admin` / `admin`** (that is what `-i base` sets), and
change that password immediately — `admin_passwd` in `config/odoo.conf` is the *database manager* master
password, not this login.

Do not add `--test-enable` to the `-i` line: on a fresh database Odoo then runs the tests of every
installed module, including core ones.

## 3. Enter the data, in this order

The order matters — later steps depend on earlier records. Menu labels are Arabic when the user language is
Arabic; the action names in brackets are the stable reference.

1. **Company** — Settings → Companies: name, address, phone, logo, currency. *Invoices* tab: one bank
   account per wallet, plus the payment title/note wording.
2. **Taxes** — Invoicing → Configuration → Taxes; and the "prices include tax" setting. Do this before
   products so each product can use the right tax.
3. **Products** — Retail Management → Products [`stock.product_template_action_product`]: price, tax,
   barcode (the till needs it), unit, category.
4. **Register and payment methods** — Retail Management → Settings
   [`point_of_sale.action_pos_configuration`]: one register with the payment methods the shop accepts,
   receipt footer. Open the session from Retail Management → Point of Sale.
5. **Users** — Settings → Users → New. Manager gets **Retail Manager**, cashier gets **Retail Cashier**
   and nothing else. Never give *Settings* / *Administrator* (`base.group_system`) to shop staff; neither
   role includes it. Set each user's language in their Preferences (Arabic is `ar_001`).
6. **Opening stock** — as the admin, Inventory → Physical Inventory (the cashier's Inventory screen is
   deliberately read-only).

## 4. Verify before handover

| Check | How | Expected |
|---|---|---|
| Module installed | `docker compose exec -T db psql -U "$POSTGRES_USER" -d "$DB_NAME" -tAc "select state from ir_module_module where name='retail_management'"` | `installed` |
| Login page | `curl -s -o /dev/null -w '%{http_code}' http://localhost:<port>/web/login` | `200` |
| Cashier's world | log in as the cashier | only **Retail Management** (5 screens) plus the Apps launcher — no Settings, no Odoo admin apps |
| Cashier is not an admin | as the cashier, try to create a product | access error (the guard is server-side, not a hidden menu — `tests/test_security.py`) |
| Invoice printout | Invoicing → create a **draft** invoice → Print → Invoice | wallets, holder names, phone and the two wordings appear; one page |
| Cashier stock screen | Retail Management → Inventory | list only, nothing editable |
| Refund guard | as the cashier, try to refund a POS order | refused with a permission error |

Use a *draft* invoice for the print test: it shows the layout without creating accounting entries. Do not
invent a test sale in the shop's database.

## 5. Hand over

- Change the `admin` password, create real named users, and give the owner their logins — no shared
  "cashier" account in a real shop.
- `scripts/backup.sh` writes the database dump + filestore into `backups/` (git-ignored); say where it is
  and that both files are needed for a restore.
- The stack answers on `127.0.0.1` only. A shop server that other devices can reach is
  `docs/DEPLOYMENT.md` — production, a human decision, and not part of this runbook.
- `git status` must be clean and nothing may be committed: the clone is the template, not a fork. Never
  push to `origin`.
- Tell the owner in plain words what you entered and what is still missing (e.g. "no logo supplied").

## 6. When the shop needs something the app does not do

That is a product change, not onboarding: it belongs upstream in the template repo (with a test and a
`DECISIONS.md` entry, per `AGENTS.md`), never as an edit in the client's clone. Stop and say so with your
recommendation instead of patching it locally.
