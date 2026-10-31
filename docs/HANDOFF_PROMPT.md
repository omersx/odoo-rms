# Handoff Prompt — paste into a new or replacement agent

Use this when you switch agents, tools, or models, or when a session was interrupted. Run it from the
project root (`~/rms`, inside WSL).

---

You are taking over the RMS project (Retail Management System on Odoo 19 Community) from a previous
agent. Do not start over.

1. Read `AGENTS.md` fully and follow it (autonomy tiers, hard stops, pre-approved actions).
2. Read `docs/PROJECT_STATE.md`, then the latest entries of `docs/DECISIONS.md`, `docs/BACKLOG.md`,
   and the current phase in `docs/DEVELOPMENT_ROADMAP.md` and `docs/RETAIL_MANAGEMENT_SPEC.md`.
3. **Verify the state against reality (do not trust the notes blindly):**
   `git status`, `git log --oneline -20`, `git tag`, `scripts/preflight.sh`, `docker compose ps`,
   and re-run the relevant tests. Compare with what PROJECT_STATE.md claims.
4. Report back briefly, then continue:
   - Where the project stands (milestone, phase, what is verified done).
   - Any discrepancy between the notes and reality, and how you fixed the notes.
   - What you will do next (the stated "Next action", adjusted if reality differs).
5. Continue working according to the autonomy level in `PROJECT_STATE.md`. Checkpoint as you go.
   Update `PROJECT_STATE.md` before you stop.

If anything in the notes is missing or contradictory and you cannot resolve it by inspection, use the
escalation format in `docs/AGENT_PLAYBOOK.md` with a recommendation; do not guess.
