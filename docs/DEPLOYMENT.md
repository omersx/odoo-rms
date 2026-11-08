# Deployment Guide — one kit for local setup and hosted server

The same Docker Compose kit runs everywhere. Only the **mode** differs.

| Mode | Where | Odoo reachable at | HTTPS | Config |
|---|---|---|---|---|
| **dev** | Your Windows PC (Docker Desktop via WSL2) | `http://localhost:8069` (this PC only) | No | `setup.sh dev` |
| **prod, local** | An always-on PC/mini-server in the shop | `https://<hostname>` on the LAN | Caddy (local CA) | `setup.sh prod <hostname>` |
| **prod, hosted** | A VPS / cloud server with a domain | `https://shop.example.com` | Caddy + Let's Encrypt | `setup.sh prod shop.example.com` |

> **Honest status:** the files were syntax-checked and `setup.sh` was tested, but the full stack has
> **not yet been run on a real Docker host**. Treat the first run as part of Phase 0/1 verification and
> record what you confirmed in `ARCHITECTURE.md`. Items marked **VERIFY** must be checked against the
> official Odoo 19 and image documentation.

## 1. Files in the kit
```text
docker-compose.yml            base: PostgreSQL + Odoo (no published DB port)
docker-compose.dev.yml        dev: publishes Odoo on 127.0.0.1:8069
docker-compose.prod.yml       prod: adds Caddy (HTTPS on 80/443); Odoo/DB not published
deployment/Caddyfile          reverse proxy rules (incl. websocket route)
config/odoo.conf.*.example    dev and prod Odoo settings templates
.env.example                  template for secrets and image tags
scripts/setup.sh              generates .env + config/odoo.conf with random secrets
scripts/preflight.sh          read-only environment check (changes nothing)
scripts/bootstrap.sh dev      one-command dev setup: config, images, database, start, readiness check
scripts/backup.sh             database dump + filestore archive
scripts/restore.sh            restore into a NEW database (never overwrites)
custom_addons/                your modules (retail_management goes here)
```
`.env` and `config/odoo.conf` hold secrets and are ignored by Git. Never commit them.

## 2. Quick start — development (Docker Desktop, run inside WSL2/Ubuntu)
**Shortcut:** `scripts/preflight.sh` then `scripts/bootstrap.sh dev` does steps below automatically (dev only;
re-runnable; never overwrites config or drops data). The AI agent uses these scripts. Manual steps:
```bash
cd ~/rms                        # project in the Linux filesystem, not /mnt/c
chmod +x scripts/*.sh           # needed if the zip was extracted on Windows
scripts/setup.sh dev
docker compose up -d db
```
Then create the database (section 3), start everything, and open `http://localhost:8069`:
```bash
docker compose up -d
docker compose logs -f odoo
```

## 3. Create the database (first time, every mode)
The production config hides the database manager, so create the database from the command line.
Use demo-free data for anything real. **VERIFY flags against the Odoo 19 CLI docs.**
```bash
docker compose run --rm odoo odoo -d "$(grep ^DB_NAME= .env | cut -d= -f2)" \
  -i base --without-demo --stop-after-init
docker compose up -d
```
For a throwaway **test** database used by automated tests, use a different name (e.g. `rms_test`) and
pass `--test-enable`, as recorded in `ARCHITECTURE.md` §2 once verified.

Install your module later (after Phase 1 exists):
```bash
docker compose run --rm odoo odoo -d <db> -i retail_management --stop-after-init   # first install
docker compose run --rm odoo odoo -d <db> -u retail_management --stop-after-init   # upgrade
```

## 4. Hosted server (VPS / cloud)

**Server:** a small Linux server (Ubuntu LTS recommended). Start with at least 2 vCPU / 4 GB RAM and
tune to load; size by number of terminals and products.

1. **DNS:** point an `A` record (e.g. `shop.example.com`) at the server's public IP.
2. **Firewall:** allow only `22` (SSH), `80`, `443`. Do **not** open `5432` or `8069`.
3. **Install Docker Engine + Compose plugin** (official Docker instructions), and Git.
4. **SSH:** key-only login, no root login, a non-root deploy user.
5. **Get the project:** clone your repository to the server (e.g. `/opt/rms`).
6. `scripts/setup.sh prod shop.example.com`
7. Review `.env` image tags; then `docker compose up -d db`, create the database (section 3),
   then `docker compose up -d`.
8. Visit `https://shop.example.com`. Caddy obtains the certificate automatically on first request
   (ports 80/443 must be reachable).
9. Complete first-run Odoo setup: company, currency, taxes, warehouse, POS, users (spec §10, CFG-*).
10. **Backups:** schedule `scripts/backup.sh` (cron, e.g. nightly) and copy backups **off the server**.
    Perform a test restore (section 6) **before** go-live.

## 5. Local store server (always-on machine in the shop)
Same as the hosted steps, with a LAN hostname instead of a public domain:
- Use `scripts/setup.sh prod pos.shop.lan` (or the machine's static IP/hostname).
- Caddy issues certificates from its **own local CA**; devices will show a browser warning until
  that CA is trusted. Export Caddy's root certificate from the `caddy-data` volume and install it on
  each POS device (**VERIFY** current Caddy docs for the path and procedure).
- Give the server a **static LAN IP** and run it on a UPS if power is unreliable.
- **Prefer a Linux machine** (or Linux VM) for an always-on shop server. Docker Desktop on Windows is
  a development tool: it stops when Windows logs out, restarts, or updates, so it is a fragile
  production host.
- Remote access from outside the shop is not enabled by this kit; use a VPN or a hosted server.

## 6. Backup and restore
```bash
scripts/backup.sh                                   # writes ./backups/<db>_<stamp>.dump + _filestore.tar.gz
scripts/restore.sh backups/rms_X.dump backups/rms_X_filestore.tar.gz rms_restore_test
```
- Restore always goes into a **new** database name; point `DB_NAME` (and `db_name`/`dbfilter` in
  `config/odoo.conf` for prod) at it, then `docker compose up -d --force-recreate odoo`.
- `backup.sh` deletes backups older than `BACKUP_KEEP_DAYS` in `BACKUP_DIR` only.
- A backup you have never restored is not a backup. Test a restore on a separate machine or database,
  and record the date and result in the roadmap progress log (Phase 8).

## 7. Moving from local to hosted
1. On the local machine: `scripts/backup.sh`.
2. On the server: complete section 4 through step 7 **but** skip creating a fresh database.
3. Copy both backup files to the server and run `scripts/restore.sh <dump> <filestore> <name>`.
4. Set `DB_NAME` / `db_name` / `dbfilter` to `<name>`, then recreate Odoo and test.
5. Keep **the same custom add-on versions and Odoo image** on both sides.

## 8. Updating safely
1. Take a backup. Try the update on a **staging copy** first.
2. Update your code: `git pull`.
3. Change `ODOO_IMAGE` only deliberately (new pinned tag/digest you have tested); never rely on a
   moving tag in production.
4. `docker compose pull && docker compose up -d`
5. Upgrade modules: `docker compose run --rm odoo odoo -d <db> -u retail_management --stop-after-init`
6. Run the smoke checklist: login, open POS, one sale, one receipt, one invoice, stock check.
7. Roll back by restoring the pre-update backup into a new DB and the previous image tag.

## 9. Production checklist
- [ ] `list_db = False`, `proxy_mode = True`, strong `admin_passwd` (generated by `setup.sh prod`).
- [ ] Only 80/443 (and SSH) reachable; DB port not published.
- [ ] HTTPS works with a trusted certificate on every POS device.
- [ ] Image tags pinned and recorded in `ARCHITECTURE.md`.
- [ ] `workers` and memory limits reviewed for the server size (**VERIFY** Odoo 19 guidance).
- [ ] Nightly backups running, copied off-machine, restore tested and logged.
- [ ] OS and Docker security updates scheduled; a person is responsible for them.
- [ ] Log monitoring and disk-space alert in place.
- [ ] Individual user accounts only; default/admin passwords changed; no demo data.
- [ ] Taxes, invoicing and currency reviewed by a qualified local adviser.
- [ ] POS printers, scanners and offline behaviour tested on target hardware (spec §6).
- [ ] Rollback procedure written and tried.

## 10. Troubleshooting
- **Odoo cannot read config:** `config/odoo.conf` must be readable by the container user (mode 644).
- **"Module not found":** check `custom_addons/` is mounted and the module has a valid manifest;
  restart Odoo and update the app list. Odoo ignores an addons directory that contains no module
  (`__init__.py` + `__manifest__.py`), so an empty `custom_addons/` logs "invalid addons directory".
- **`docker compose pull` returns 403 "CloudFront ... block access from your country":** Docker Hub's
  blob CDN is geo-blocked. Use a registry mirror with the same digests (e.g. `mirror.gcr.io/library/...`)
  in `ODOO_IMAGE`/`POSTGRES_IMAGE`, or a VPN; verify digests with `docker buildx imagetools inspect`.
  `scripts/bootstrap.sh dev` keeps the official tags by default, so set the mirror in `.env` in that case.
- **Websocket/POS live updates fail behind the proxy:** confirm `workers > 0`, the `/websocket`
  route to port 8072 in `deployment/Caddyfile`, and `proxy_mode = True` (**VERIFY** in Odoo 19 docs).
- **Certificate error on LAN:** the Caddy local CA is not trusted on that device (section 5).
- **Danger — deletes data:** `docker compose down -v`, `docker volume rm`, `docker system prune`.
  The agent must ask before running them.

## 11. First store setup (new database)

Do this once per database, as the administrator, in this order. Nothing here is custom code — it is
native Odoo configuration.

1. **Country, currency, taxes** (Invoicing → Settings):
   - *Fiscal Country* and the company country = **Sudan**, *Currency* = **SDG**, *Prices* = **Tax Included**.
   - Set the currency symbol to `SDG` (Invoicing → Configuration → Currencies → SDG → Symbol), otherwise
     amounts render with the Arabic `ج.س.`. **Restart the server afterwards** — currency symbols are cached
     per worker and do not refresh on their own.
   - Default *Sales Tax* and *Purchase Tax* = **0%** (amount 0, price included).
   - Leave *Package* on **Generic Chart of Accounts**: Odoo 19 Community has **no Sudan localization**
     (`l10n_sd` does not exist), and installing a neighbouring country's pack would file the books under
     foreign accounts and tax law.
   - Do this **first**: Odoo refuses to change the company currency once any journal entry exists.
   - After changing the country, open Configuration → Taxes and check they no longer say `(US)`.
     `account.tax.country_id` does not follow the company country automatically; it must be set to Sudan
     together with a Sudan tax group (details in `ARCHITECTURE.md` §7.2).
2. **Module:** install *Retail Management* (`custom_addons/retail_management`).
3. **Users** (Settings → Users): one account per person. Assign exactly one retail group:
   - *Retail Cashier* → checkout only.
   - *Retail Manager* → products, stock, customers, invoices, POS configuration, refunds.
   Never give a cashier `account.group_account_invoice`: Odoo then treats them as a POS manager.
4. **Cash journal** (Invoicing → Configuration → Journals): create type *Cash* if none exists.
5. **Payment method** (Point of Sale → Configuration → Payment Methods): name `Cash`, journal = the cash
   journal above. For each mobile wallet (Bankak, Fawry, …) create **its own Bank journal** first, then the
   method on that journal, so each wallet books to its own account and is reported separately. Optionally
   set an `image` per method — the till shows it as the button's icon.
6. **Point of Sale → Configuration → Settings**: create/open the register, add the `Cash` payment
   method, enable *Restrict Price Modifications to Managers*, enable cash control if you want drawer
   counts, and enable **Set Maximum Difference** with a small amount (10,000 SDG ≈ 1 USD): a cashier can
   then not close a session whose drawer is off by more than that, a manager must accept it (D-016).
   Set the picking type to `PoS Orders`.
7. **Products** (Retail Management → Products): name, price, cost, unit, barcode, internal reference;
   tick *Available in POS* and make the product storable so stock is tracked.
8. **Stock** (Retail Management → Inventory): receive starting quantity with a standard receipt;
   corrections via inventory adjustment (managers only).
9. **Owner:** change the default `admin` password before anyone else uses the server.
