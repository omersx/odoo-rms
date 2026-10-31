# Windows Development Setup — Docker Desktop or WSL2 + Ubuntu

Both options are supported. **Pick one per project** and record the choice in `ARCHITECTURE.md` §2.
Everything here is a starting point: **verify versions, image tags and package names against the
official Odoo 19 documentation and the Odoo 19 `requirements.txt` before relying on them.**

## 1. Which option?

| | **Option 1 — Docker Desktop** | **Option 2 — WSL2 + Ubuntu (native Odoo)** |
|---|---|---|
| Best when | You already have Docker Desktop and want a clean, reproducible setup | You want to read/debug Odoo source directly and run it like a Linux server |
| Setup effort | Low | Medium |
| Reproducible on another PC | Excellent | Manual |
| Reading Odoo source | Via the container or a mounted copy | Direct, in a normal folder |
| Debugging | Possible, needs container-aware setup | Simplest |
| Closest to a typical Linux production | Yes (if production uses containers) | Yes (if production is a plain Linux server) |
| Resource use | Higher (Docker VM + containers) | Lower |

**Recommendation:** with Docker Desktop already installed, start with **Option 1**. Switch to Option 2
if you need deeper source-level debugging. The custom add-on code is identical either way.

## 2. Rules that apply to both

- Both options need **WSL2** on Windows (Docker Desktop uses it as its backend).
- **Keep the project in the Linux filesystem** (e.g. `~/rms` inside Ubuntu), **not** under
  `/mnt/c/...`. Bind mounts from `C:` are slow and can break file watching and permissions.
- Run **OpenCode and Git inside WSL**, in the project folder. The agent then uses Linux commands
  (`docker compose ...`, `python`, `psql`) exactly as its instructions assume.
- Use a **disposable test database**. Never point development at real business data.
- Use **VS Code with the WSL extension** (or any editor that opens the WSL folder).
- Open Odoo from Windows at `http://localhost:8069` (check the port in your config).
- **Never commit secrets.** Keep passwords in a `.env` file listed in `.gitignore`.
- Custom code goes in `custom_addons/`. Never edit Odoo core, in either option.

## 3. Option 1 — Docker Desktop

### Prerequisites
1. Docker Desktop installed, with the **WSL2 backend** enabled.
2. Docker Desktop → Settings → Resources → **WSL integration**: enable it for your Ubuntu distro.
3. In Ubuntu, confirm: `docker --version` and `docker compose version`.

### Use the ready-made kit
The repository root already contains a Docker kit (compose files, Caddy proxy, config templates,
setup/backup/restore scripts). **Do not write your own compose file.** Follow `DEPLOYMENT.md`:
- Fast path: `scripts/preflight.sh` then `scripts/bootstrap.sh dev` (the AI agent runs these).
- Or manually: `scripts/setup.sh dev` creates `.env` and `config/odoo.conf` with random passwords.
- `docker compose up -d db`, create the database (`DEPLOYMENT.md` §3), then `docker compose up -d`.
- The same kit later runs on a local store server or a hosted server (`DEPLOYMENT.md` §4–5).

Image tags (`ODOO_IMAGE`, `POSTGRES_IMAGE` in `.env`) must be **verified**, and the working install,
upgrade and test commands recorded in `ARCHITECTURE.md` §2.

Odoo source for the agent to inspect: read it inside the container (verify the path, commonly under
the Python `dist-packages`), or copy it out read-only for reference. Never edit it.

### Docker safety
- `docker compose down -v`, `docker volume rm`, and `docker system prune` **delete data**. The agent
  must ask before running them (see AGENTS.md).
- Pin the image tag/digest you validated so the build does not change silently.

## 4. Option 2 — WSL2 + Ubuntu (native Odoo)

### Steps (outline — verify against official Odoo 19 install docs)
1. PowerShell as administrator: `wsl --install -d Ubuntu-24.04`, restart, create your Linux user.
2. Inside Ubuntu: install Git, Python 3 with `venv` and dev headers, build tools, PostgreSQL, and the
   system libraries listed in Odoo's documentation (e.g. for lxml, LDAP, PDF rendering).
3. Create a PostgreSQL role for Odoo (not a superuser account used for anything else).
4. Clone Odoo Community from the official GitHub repository, branch `19.0`, into `~/odoo/odoo`
   (read-only reference; never edit it).
5. Create a virtual environment and install `requirements.txt` from that checkout.
6. Create `~/rms/config/odoo.conf` with `addons_path` including Odoo's addons and
   `~/rms/custom_addons`, and DB credentials (not committed).
7. Run: `python ~/odoo/odoo/odoo-bin -c ~/rms/config/odoo.conf` (confirm the exact path/command).
8. Tests: `... -d rms_test -i retail_management --test-enable --stop-after-init`.

### Notes
- Record the exact Odoo commit (`git rev-parse HEAD`) in ARCHITECTURE.md §2.
- PDF reports may need a `wkhtmltopdf` build compatible with Odoo — verify the version Odoo 19
  recommends before testing invoice printing.

## 5. Both options — checklist before Phase 1
- [ ] Odoo starts and the login page opens at `http://localhost:8069`.
- [ ] A disposable test database exists and can be recreated.
- [ ] `custom_addons/` is in `addons_path` and visible to Odoo.
- [ ] The install/upgrade and test commands work and are recorded in `ARCHITECTURE.md` §2.
- [ ] Odoo version/revision and PostgreSQL version are recorded.
- [ ] `.env` and any `odoo.conf` containing passwords are ignored by Git.
- [ ] A backup/restore method for the dev database is known (needed again in Phase 8).

## 6. Windows-specific cautions
- **Printers and barcode scanners** must be tested on the real Windows device in the browser
  (Phase 8). Neither Docker nor WSL2 changes how the browser talks to hardware, but network/USB
  access differs from a Linux machine.
- **Line endings:** configure Git with `core.autocrlf=input` in WSL to avoid CRLF problems in scripts.
- **Memory:** if Docker/WSL feels slow, cap WSL memory in `%UserProfile%\.wslconfig`, and give Odoo
  enough RAM (16 GB host recommended).
- **Antivirus** scanning of the WSL filesystem can slow Odoo; exclude the project folder if needed.
