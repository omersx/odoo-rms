# Industry variants — one codebase, many shops

The base add-on (`retail_management`) is a **retail skin over native Odoo**, not a product for one
specific trade. When a second industry appears (pharmacy, bakery, electronics…), do **not** copy the
repository or branch it. Add a thin module that depends on the base.

## The rule

```
custom_addons/
  retail_management/          ← shared base: roles, server guards, launcher, POS polish, receipt
  retail_bakery/              ← depends on retail_management; only what actually differs
  retail_pharmacy/            ← depends on retail_management; only what actually differs
```

A variant module should stay **small** — a handful of fields, a report, a default, an extra guard.
If a change is useful to every shop, it belongs in the base, not in the variant, so that every shop
gets the fix when you upgrade.

## Configuration before code

Check these native Odoo 19 Community capabilities first. Most "industry" requirements are settings,
not modules.

| Industry need | Native answer | Where |
|---|---|---|
| Expiry dates / batches (pharmacy, food) | `product_expiry` + lots/serials on `stock` | install the module, set tracking |
| Serial numbers (electronics) | built-in serial tracking | product → Tracking |
| Weight / partial units (bakery, deli) | Units of Measure with decimal quantity | product UoM |
| Sizes, colours, pack sizes | product attributes and variants | product → Attributes |
| Wholesale vs retail pricing | pricelists | config |
| Different tax per category | taxes on product category | config |
| Register-type behaviour per shop | multiple POS configs | config |
| Receipts with shop name/logo | company settings + `receipt.scss` | config |

If a requirement is satisfied by one of these, **write no code**. Write a checklist for that shop
instead.

## When a variant module is justified

- A field that only that trade needs (e.g. `prescription_ref` on the order line).
- A workflow rule (e.g. "a lot must be selected before paying").
- A report the trade regulator wants.
- A default or a menu arrangement that saves the operator daily work.

## Creating one

1. `mkdir custom_addons/retail_<industry>/` with `__init__.py` and `__manifest__.py`:
   ```python
   {
       "name": "Retail <Industry>",
       "version": "19.0.1.0.0",
       "license": "LGPL-3",
       "category": "Sales/Point of Sale",
       "depends": ["retail_management"],
       "data": ["views/..."],
       "installable": True,
   }
   ```
2. Add **only** the delta: fields (`_inherit`), views (`inherit_id` + `xpath`), server checks,
   reports. Never copy base code into it.
3. Add a test in `tests/` for anything you add that decides money, stock or permission — and test the
   **denied** path, not only the allowed one.
4. Install it on a disposable database together with the base:
   `odoo -d rms_test -i retail_<industry> --test-tags /retail_<industry>`.
5. Document the shop-specific settings in that shop's own notes, **not** in the variant's code.

## What must never go into a variant

| Do not | Why |
|---|---|
| A copy of the refund / stock guards | Two sources of truth; a fix will miss one shop |
| Its own permission groups | The base roles are the security model; extend, don't fork |
| A branch of the repository per customer | Fixes stop flowing; removals become impossible |
| Odoo core edits | Upgrades break, support ends |
| Customer data, logos, prices, DB dumps | Belongs in that shop's database, never in Git |
| A tax/legal rule hard-coded in Python | Tax is configuration and a business decision |

## Deploying a variant

Same Docker kit, one database per shop, one `.env` per shop:

```
shop A: --db rms_a, module retail_management
shop B: --db rms_b, module retail_management + retail_pharmacy
```

Record which **git tag** runs on which shop, so "what is deployed where" is a fact you can check.

## Anti-patterns seen in the wild

- **Forked repo per client** — six months later, five versions of the same guard.
- **`if customer == "X"` in shared code** — hidden branches nobody tests.
- **A "general" module loaded with every possible feature** — every shop pays the complexity cost.
- **Variants that override the base's files** — instead of extending, they silently drop later base
  fixes.
