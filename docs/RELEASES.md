# Releases — what a shop runs, and how to move it

**A shop runs a tag, never `main`.** The tag equals the module version (`19.0.1.18.0` →
`v19.0.1.18.0`) because that is the number Odoo itself compares when it upgrades a database.

## Cut a release (template repo, development mode)

1. `git status` clean, the CI run on `main` green, and the fresh-clone drill done (`docs/CLIENT_ONBOARDING.md`).
2. Bump `"version"` in `custom_addons/retail_management/__manifest__.py` (e.g. `19.0.1.18.0` → `19.0.1.19.0`).
3. Add the same version as a section in `CHANGELOG.md`, with the Odoo build it was verified on.
4. Commit, then:

```bash
git tag -a v19.0.1.19.0 -m "Release 19.0.1.19.0"
git push origin main && git push origin v19.0.1.19.0
```

No release script: a guard around `git tag` is one more thing to trust, and the tag itself is the record.

## Install a shop on a release

```bash
git clone https://github.com/omersx/odoo-rms.git ~/rms-<client>
cd ~/rms-<client>
git checkout v19.0.1.18.0
scripts/setup.sh dev      # then edit COMPOSE_PROJECT_NAME / DB_NAME / ODOO_PORT in .env
scripts/bootstrap.sh dev
```

Record which tag runs where in that shop's own notes (`CLIENT_NOTE.md`, or a private client-config repo).

## Update a live shop

Never `git pull` a running shop. An upgrade is a staged operation:

1. `scripts/backup.sh` and copy the dump off the machine. A backup you have not restored once is a guess.
2. Restore that dump into a **staging** database on the same stack.
3. `git checkout v<new>` in a second clone (or after stopping Odoo), and upgrade **staging**:

```bash
docker compose run --rm odoo odoo -d <staging_db> -u retail_management --stop-after-init
docker compose run --rm odoo odoo -d <staging_db> -u retail_management --test-enable --stop-after-init
```

4. Open staging, do a sale, print a receipt and an invoice. On failures: stop, report, do not touch production.
5. On success: backup production, upgrade it, smoke test, and note the new tag.

## Roll back

Restore the backup taken in step 1 and `git checkout v<previous>`. A database upgraded by a newer module
version cannot be downgraded by the older code, which is why the backup — not the tag — is the rollback.
