# RMS — OpenCode project documentation

Documentation pack for building a lightweight Retail Management System on **Odoo 19 Community**
with OpenCode.

## Contents
| File | Purpose |
|---|---|
| `AGENTS.md` | Rules OpenCode loads automatically from the repo root. |
| `INITIAL_PROMPT.md` | First prompt to paste into OpenCode (environment setup + discovery). |
| `docs/RETAIL_MANAGEMENT_SPEC.md` | What to build: scope, roles, requirements, acceptance tests. |
| `docs/ARCHITECTURE.md` | Environment facts and verified technical decisions (agent fills in). |
| `docs/DEVELOPMENT_ROADMAP.md` | Phases, milestones, approval gates, progress log. |
| `docs/PROJECT_STATE.md` | Live handoff memory: current task, next action, blockers, autonomy level. |
| `docs/DECISIONS.md`, `docs/BACKLOG.md` | Decision log; parked ideas awaiting your approval. |
| `docs/AGENT_PLAYBOOK.md`, `docs/HANDOFF_PROMPT.md` | Debug/decide/escalate procedures; prompt for a replacement agent. |
| `CLAUDE.md` | One-line pointer so other agent tools read `AGENTS.md`. |
| `docs/WINDOWS_SETUP.md` | Windows dev setup: Docker Desktop **or** WSL2 + Ubuntu. |
| `docs/OPTIONAL_TOOLS.md` | How to evaluate optional tools such as the Odoo Architect framework. |
| `docs/DEPLOYMENT.md` | Local setup and hosted-server deployment with the Docker kit. |
| `docker-compose*.yml`, `deployment/`, `config/`, `scripts/`, `.env.example` | Ready-to-use Docker kit. |

## Setup — the agent does most of it

**You do once (Windows, about 15 minutes; the agent cannot do these):**
1. Install **Docker Desktop** and enable Settings → Resources → **WSL integration** for your Ubuntu distro.
   (If you have no Ubuntu: PowerShell as administrator → `wsl --install -d Ubuntu-24.04`, restart.)
2. In the **Ubuntu terminal**:
   ```bash
   sudo apt update && sudo apt install -y unzip git openssl curl
   mkdir -p ~/rms && cd ~/rms
   unzip /mnt/c/Users/<YourWindowsName>/Downloads/RMS_OpenCode_Documentation_v6.zip -d .
   chmod +x scripts/*.sh
   ```
   Keep the project in `~/rms`, **not** under `/mnt/c`.
3. Install **OpenCode** inside Ubuntu (official instructions at opencode.ai) and connect your model
   provider.
4. Start it: `cd ~/rms && opencode`, then paste the prompt from `INITIAL_PROMPT.md`.

**The agent then does:** preflight checks → creates `.env` and `config/odoo.conf` with random secrets →
pulls images → creates the database → starts Odoo → records the verified versions in the docs →
Git commit → discovery → report. It stops for your approval.

**You then:** open http://localhost:8069, **change the default admin password**, read the report, and
reply "Approved. Proceed with Milestone A, Phase 1 only."

The agent may only run the actions listed in `AGENTS.md` ("Pre-approved actions"). It must ask for
`sudo`, Docker/WSL changes, deleting data, production mode, pushing to a remote, or opening ports.

Manual route (no agent): `scripts/preflight.sh` then `scripts/bootstrap.sh dev`.

## Autonomy and memory
- **Autonomy:** the agent decides *how* to build (design, debugging, trade-offs) and records decisions in
  `docs/DECISIONS.md`. It asks you only for **hard stops** (scope changes, deleting data, security,
  secrets, sudo/system changes, production, pushing code, tax/legal choices). Ideas that would add
  features go to `docs/BACKLOG.md` for you to approve. Change the level on the `autonomy:` line of
  `docs/PROJECT_STATE.md`: **1** stop every phase · **2** stop at milestones (default) · **3** report
  and continue.
- **Memory:** `docs/PROJECT_STATE.md` is the live handoff file (where we are, next action, blockers);
  Git commits and tags are the ground truth. The agent updates both as it works.
- **Switching agents:** start the new agent in `~/rms` and paste `docs/HANDOFF_PROMPT.md`. It reads the
  state, verifies it against reality, and continues. `CLAUDE.md` simply points other tools to `AGENTS.md`.
- **Test it once:** after Phase 0, start a fresh session with `HANDOFF_PROMPT.md` and check that it can
  say what is done and what is next *without* your help. If not, the state file needs improving.

## How the work flows
1. **Phase 0 – Discovery.** The agent inspects only; it reports and waits for you.
2. **Milestone A – Working core:** module, roles, products/stock, POS. Review before continuing.
3. **Milestone B – Complete MVP:** invoicing, simple customer management, dashboard/reports.
4. **Milestone C – Release readiness:** offline tests, backup/restore, hardware, guides.

After each gate, read the agent's report (verified facts vs assumptions, tests run, limitations), then
reply "approved, continue with Milestone X" or give corrections.

## Tips
- Begin with plain OpenCode plus `AGENTS.md`. Add optional tools (Superpowers, Planning with Files,
  Odoo Architect Framework) only if you actually need them and they are installed and discoverable.
- Keep the spec as the single source of scope. Change scope by editing the spec yourself, not by
  chatting; then tell the agent to re-read it.
- Commit to Git after each approved phase so you can roll back.
- If the agent seems to guess model/field names, tell it: "verify in the Odoo 19 source first."
- Have a qualified local adviser review taxes and invoicing before real transactions.
