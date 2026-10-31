# PROJECT STATE — live handoff file

> **Overwrite this file; do not append endlessly.** Keep it under ~100 lines. It is the first thing a
> new agent reads. Detailed history belongs in Git, `DECISIONS.md` and the roadmap, not here.
> If this file disagrees with the repository or running system, trust reality and fix this file.

**Last updated:** 2026-10-31 · OpenCode 1.19.1 · model `opencode/deepseek-v4.1-flash-free`
**autonomy:** 2          <!-- owner edits: 1 = guided, 2 = standard (default), 3 = high -->

## Where we are
- Milestone: A · Phase: 0 (Stage 0 environment + discovery) · Status: **BLOCKED at Stage 0**
- Roadmap reference: `docs/DEVELOPMENT_ROADMAP.md` (do not copy its checklist here)

## Current task
None. Stage 0 stopped on two preflight FAILs the agent is not allowed to fix. Phase 0 discovery has not
started; it needs a running Odoo to verify versions, module manifests, groups and offline behaviour.

## Last completed (newest first, max 8)
- 2026-10-31: Read the documentation pack; inspected repo, Docker kit, `.gitignore`, OpenCode setup.
- 2026-10-31: Ran `scripts/preflight.sh` inside WSL Ubuntu 24.04. Result: 2 FAIL, 1 WARN.
  - FAIL: project is under `/mnt/c/Users/Wad Yonis/Desktop/odoo-app` (must live in the Linux filesystem).
  - FAIL: Docker daemon not reachable from Ubuntu (`/var/run/docker.sock` absent; Docker Desktop WSL
    integration for Ubuntu is off — `EnableIntegrationWithDefaultWslDistro=false`).
  - WARN: 3 GB RAM visible to WSL (4+ GB recommended).
- 2026-10-31: `git init` + initial commit of the documentation/kit baseline.

## Next action (concrete)
Owner: follow `docs/WINDOWS_SETUP.md` §7 (manual steps in the Stage 0 report / below), then:
1. Reopen OpenCode in `~/rms` inside Ubuntu (not `/mnt/c`).
2. Run `scripts/preflight.sh` → expect 0 failures.
3. Run `scripts/bootstrap.sh dev` → expect HTTP 200 at `http://localhost:8069`.
Agent then records the printed versions/image digests in `ARCHITECTURE.md` §2 and starts Phase 0 discovery.

## In-flight / uncommitted work
None.

## Blockers and questions for the owner
1. **Project on `/mnt/c`** — move it to `~/rms` in WSL (agent must not do this; it changes the owner's
   workspace). Keep the Windows copy until the WSL copy is verified.
2. **Docker Desktop WSL integration for Ubuntu is disabled** — enable it in Docker Desktop settings and
   restart Docker; the agent cannot change Docker/WSL settings.
3. WSL sees only 3 GB RAM (warning). Owner decides whether to raise it in `%UserProfile%\.wslconfig`.

## Decisions pending owner review
None.

## Environment quick facts (full detail: `ARCHITECTURE.md` §2)
- Host: Windows 10 22H2 (10.0.19045) · WSL2 Ubuntu 24.04.2 LTS · kernel 6.18.54.1
- Docker CLI 29.8.0 · Compose 5.5.1 (clients verified; daemon **not** reachable from Ubuntu)
- Dev URL after bootstrap: http://localhost:8069 · Start: `docker compose up -d` · Logs: `docker compose logs -f odoo`
- Test command: (fill in once verified)
- Dev DB: `rms` · disposable test DBs: `rms_test*`

## Known issues / tech debt
- Stage 0 blocked by environment (above). Nothing else recorded.

## Recent session log (rolling, last 10 — newest first)
| Date | Agent/tool | What happened |
|---|---|---|
| 2026-10-31 | OpenCode / deepseek-v4.1-flash-free | Stage 0 preflight failed (path + Docker integration); docs/state updated, baseline committed, stopped for owner action |
