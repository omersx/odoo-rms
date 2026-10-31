# Agent Playbook

How to work autonomously and safely. `AGENTS.md` holds the rules; this holds the procedures.

## 1. Debugging protocol (when something fails)
1. **Reproduce** with the smallest command; capture the exact error and logs
   (`docker compose logs --tail 100 odoo`).
2. **Hypothesize** 2–3 causes; rank by likelihood. Check the Odoo 19 source and official docs rather
   than guessing.
3. **Test the cheapest hypothesis first.** Change one thing at a time.
4. **Fix the root cause**, not the symptom. Never skip a test, weaken a permission, or hard-code
   around a failure.
5. **Verify:** re-run the failing check and the nearby tests; confirm nothing else broke.
6. **Record:** a short note in `PROJECT_STATE.md` ("known issues" if unresolved); a `DECISIONS.md`
   entry if the fix involved a real choice.
7. **Stuck rules:** same approach fails 3 times → change approach. Two distinct approaches fail, or
   the fix needs a Hard-stop action → escalate (§3).

## 2. Making a decision
1. Is it a Hard stop? → escalate. Otherwise continue.
2. List realistic options (usually 2–3). Prefer: native Odoo over custom; smaller over larger;
   reversible over irreversible; secure over convenient; boring over clever.
3. Check evidence (source, docs, a quick experiment on a disposable DB).
4. Pick one. Tier 2 → log with alternatives and how to reverse, and flag for review. Tier 1 → log only
   if a future reader would wonder "why?".

## 3. Escalation format (use when you must stop and ask)
```
ESCALATION — <short title>
Problem: what is blocked, and why it matters.
Evidence: commands, errors, file paths.
Tried: approaches and results.
Options: A / B / C with pros and cons.
Recommendation: <your pick and why>.
If no reply: <what you will do meanwhile, safely — e.g. continue with an unrelated task>.
```
The owner may reply "go with the recommendation". Make the recommendation one you would stand behind.

## 4. Checkpoint procedure (end of any meaningful step)
1. Run the relevant tests. 2. `git add` and commit (`phase-N: <summary>`). 3. Update
`PROJECT_STATE.md` (where we are, last completed, **next action**, blockers, in-flight work).
4. Tick the roadmap box only with evidence. 5. Add `DECISIONS.md`/`BACKLOG.md` entries if needed.
Tag finished phases: `git tag phase-N-done`.

## 5. Report format (end of phase / milestone / when stopping)
- **Done:** what changed (files), what was verified (commands + results).
- **Not verified / limitations.**
- **Decisions to review** (Tier 2 IDs with one-line summaries).
- **Ideas parked** (BACKLOG IDs).
- **Risks and blockers.**
- **Next action.**

## 6. Context hygiene
- Don't paste huge files or logs into the conversation; read ranges and grep.
- Re-read `PROJECT_STATE.md` and recent `DECISIONS.md` after long work to re-anchor.
- If your context is getting heavy, checkpoint (§4) **before** it overflows, so a fresh session loses nothing.

## 7. Handoff checklist (before you stop for any reason)
- [ ] Tests run; failures recorded, not hidden.
- [ ] Everything committed, or listed under "In-flight work" with how to continue.
- [ ] `PROJECT_STATE.md` updated, incl. a concrete **Next action**.
- [ ] Decisions logged; blockers and questions written down.
- [ ] Dev stack left in a sane state (note if anything is stopped).
