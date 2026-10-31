# Initial OpenCode Prompt — RMS Project

Paste everything below the line into OpenCode, from the project root (`~/rms`, inside WSL).

---

Act as a senior Odoo 19 Community architect and careful technical lead.

Read, in order: `AGENTS.md`, `docs/RETAIL_MANAGEMENT_SPEC.md`, `docs/ARCHITECTURE.md`,
`docs/DEVELOPMENT_ROADMAP.md`, and skim `docs/WINDOWS_SETUP.md`, `docs/DEPLOYMENT.md` and
`docs/OPTIONAL_TOOLS.md`. Follow AGENTS.md strictly, including its autonomy tiers, hard stops and pre-approved actions. Work
autonomously: analyze problems, decide, and record decisions; escalate only for Hard stops or when
stuck, using the escalation format in `docs/AGENT_PLAYBOOK.md`. Also read `docs/PROJECT_STATE.md`.

## Your task now: Stage 0 (set up the environment) then Phase 0 (discovery). No application code.

### Stage 0 — Environment bootstrap (you may do this yourself)
1. Run `scripts/preflight.sh`.
   - If it reports FAIL items you are not allowed to fix (Docker Desktop not installed or not
     integrated with WSL, missing `apt` packages, project under `/mnt/c`), **stop** and give me the
     exact manual steps, in order. Do not use `sudo` and do not try to install Docker or WSL.
2. If preflight passes, run `scripts/bootstrap.sh dev`. If it fails, read the error output and logs,
   diagnose the cause, and fix **project files** (compose files, config templates, scripts) if that is
   the problem. Re-run. Explain every fix. Do not weaken security to make it work.
3. Verify `git check-ignore .env config/odoo.conf` confirms both are ignored. Never print their contents.
4. Record the environment facts that `bootstrap.sh` prints (Docker, Compose, Odoo and PostgreSQL
   versions, image tags/digests, project path, working commands) in `docs/ARCHITECTURE.md` §2.
   Mark the Docker kit as verified or list what failed. Update the roadmap progress log.
5. `git init` if needed and make one initial commit (never push). Update `docs/PROJECT_STATE.md`
   (date, agent/tool, where we are, concrete next action) — it is the handoff file for any future agent.
6. Tell me that Odoo is running at http://localhost:8069 and remind me to change the default admin
   password.

### Phase 0 — Discovery (read-only; fill `docs/ARCHITECTURE.md` §4 and §6.1)
1. Repository state, branch, existing modules and conventions.
2. The real Odoo 19 version/revision and PostgreSQL version, addons paths, and the working commands
   to start Odoo, install/upgrade a module, and run tests (try them on a disposable `rms_test` database).
3. Which standard modules exist in this Community build and their real manifest dependencies:
   `point_of_sale`, `stock`, `account`, `contacts`, `product`, `barcodes`, and any POS-stock or
   purchasing modules. Flag anything the spec assumes but Community does not provide.
4. The actual security groups for POS, stock, accounting and contacts, and how POS cashier/employee
   access works in this build.
5. What OpenCode tooling is really present (version, `opencode.json`, agents, skills, MCP servers,
   plugins). Do not assume installed means integrated.
6. Whether native POS offline behaviour exists in this build and what it covers (read source/docs;
   testing comes later).
7. What can be done by configuration alone versus what needs custom code.

## Report format
- Stage 0 result: what ran, what you fixed, current status of the stack
- Verified facts (with file paths or commands as evidence)
- Unverified items and blockers
- Proposed minimal add-on structure and manifest dependencies
- Proposed Administrator/Cashier group mapping
- Conflicts between the spec and Odoo reality
- Decisions to review (Tier 2 IDs) and ideas parked in BACKLOG
- Questions for me (maximum five, most important first)
- Recommended plan for Milestone A (roadmap Phases 1–4)

Then STOP and wait for my approval. Do not start Phase 1.
