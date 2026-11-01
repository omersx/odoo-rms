# Decision Log

Append-only. One entry per non-trivial decision, written **when the decision is made**. Tier is from
`AGENTS.md` (1 = decided, 2 = decided and flagged for owner review, 3 = owner decided).
The owner can reverse any Tier 2 entry; mark it `Reversed` and note why.

| ID | Date | Tier | Decision | Alternatives considered | Rationale and evidence | Reversible how | Status |
|---|---|---|---|---|---|---|---|
| D-001 | 2026-11-01 | 2 | Use `mirror.gcr.io/library/*` refs for the Odoo and PostgreSQL images in this dev environment | A) official Docker Hub tags (blocked here); B) VPN/HTTP proxy (owner-controlled); C) build images from source (heavy, unverified) | Docker Hub's blob CDN returns `403 — "The Amazon CloudFront distribution is configured to block access from your country"` for every layer while auth/manifests work. `mirror.gcr.io` serves the same official images: `docker buildx imagetools inspect` gives identical manifest digests (odoo `27f920e0…`, postgres `5db6dac2…`). | Set `ODOO_IMAGE`/`POSTGRES_IMAGE` back to official tags in `.env`; nothing in the repo depends on the mirror | Needs owner review |

**Status values:** `Accepted` · `Needs owner review` · `Reversed` · `Superseded by D-xxx`

## Entry template (copy into the table, or use a section below for long entries)
- **Decision:** what was decided, in one sentence.
- **Context:** the problem or ambiguity.
- **Options:** A, B, C with one-line pros/cons.
- **Choice and why:** include evidence (file path in the Odoo 19 source, test result, command output).
- **Consequences / how to reverse.**
