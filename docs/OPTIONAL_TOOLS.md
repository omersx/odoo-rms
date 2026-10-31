# Optional External Tools

**None of these are required.** The project works with plain OpenCode plus `AGENTS.md` and the three
core documents. Add a tool only if it clearly helps, and only after it has been evaluated as below.

## 1. Rules for any third-party tool
1. **Keep it outside the RMS repository** (e.g. `~/tools/<name>`), read-only. Never copy its
   `AGENTS.md`, `CLAUDE.md`, `SYSTEM.md`, adapter folders or scripts into the RMS repo root: they would
   overwrite or compete with this project's `AGENTS.md` and bloat the agent's context.
2. **Read before you run.** Skim its instructions and code. Install CLIs in a virtual environment, pin
   the commit you reviewed, and never run its scripts with access to secrets, production data, or the
   Docker socket of a production host.
3. **MCP servers and plugins execute local code.** Treat them like any installed program. Do not put
   credentials in their config files.
4. **Its advice is a suggestion, not authority.** Anything it recommends must still be verified in the
   Odoo 19 source (AGENTS.md rule 2) and must respect the spec's scope.
5. **Record the decision** (adopted, rejected, or trial) in `DECISIONS.md` with the date and
   the reason. Do not install duplicates of tools OpenCode already provides.

## 2. Odoo Architect Agent Framework
Repository: `https://github.com/omersx/odoo-architect-agent-framework`

### Snapshot (reviewed 2026-10-31 — re-check before relying on it)
- An open-source instruction set plus Python CLI (`odoo-architect`: `info`, `doctor`, `validate`,
  `review`, `scaffold`, `smoke-test`), LGPL-3.0-or-later, with adapters for several AI tools including OpenCode.
- Very young: about 5 commits, no stars or forks, one author, self-described **release candidate**.
  Its own README says full production certification requires live Odoo 18 **and** 19 install/update
  smoke tests that were not yet shown as passed.
- Its OpenCode adapter says the agent file's metadata may need adapting to your OpenCode version, so
  discovery by OpenCode is **not guaranteed**.
- Only the README and `OPENCODE.md` were read. Its rules, patterns and checklists were **not** reviewed.
- Mismatches with RMS scope: hub-and-spoke module layout, industry playbooks (e.g. pharmacy), and a
  CRM-based sample add-on. RMS uses one small module, no regulated-industry workflows, and no CRM
  beyond native Contacts.

### Verdict
**Optional reference and second-opinion checker. Not a dependency.**

### Evaluation procedure (do this before adopting anything)
1. Clone it outside the repo: `git clone <url> ~/tools/odoo-architect` and note the commit hash.
2. Read `SYSTEM.md`, `system/`, `patterns/`, `checklists/` and `workflows/`. For each item, decide:
   *adopt* (genuinely useful and consistent with AGENTS.md), *adapt*, or *reject* (conflicts with scope
   or Odoo 19 reality). Check each adopted claim against the Odoo 19 source.
3. Copy only short, verified guidance into `ARCHITECTURE.md` (with the source file named) or the
   relevant checklist. Do not copy its files wholesale.

### Optional trial (after Phase 1 produces a real `retail_management` module)
1. In a throwaway virtual environment: `python -m pip install -e ~/tools/odoo-architect` (confirm the
   current instructions in its README and `docs/install-and-use.md`; check `odoo-architect --help`).
2. Run its static checks **against `custom_addons/retail_management`** only (e.g. `odoo-architect
   review <path>` / `validate` — confirm exact usage). Do not use `scaffold` for RMS.
3. Triage each finding: verify against Odoo 19 source, then fix, reject, or note it. Record the outcome.
4. Keep using it only if it produced at least one *verified, useful* finding and no misleading advice.

### Do not
- Use `scaffold`, the hub-and-spoke layout, or the industry playbooks for RMS.
- Use its Docker smoke-test against the RMS database or any real data.
- Let it replace this project's `AGENTS.md`, spec, or approval gates.

## 3. Other tools (not evaluated here)
- **Superpowers / Planning with Files:** use only if actually installed and discoverable in OpenCode;
  keep any `task_plan.md` / `progress.md` short and never duplicate the roadmap.
- **Other public Odoo skill/agent packs** exist (for example the same author's `mcp-odoo-architect`
  MCP server, which describes its generated add-ons as *review scaffolds, not production code*, and
  community packs such as `unclecatvn/agent-skills`, which advertise version-pinned Odoo guidance).
  These were seen only through listings and **have not been reviewed**. Apply §1 and §2's evaluation
  procedure before using any of them.

## 4. Decision record
| Date | Tool | Decision (adopted / trial / rejected) | Reason / evidence |
|---|---|---|---|
| | Odoo Architect Agent Framework | Not adopted (optional) | See §2 |
