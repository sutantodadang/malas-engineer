# AGENTS.md

This repository contains the Malas Engineer skill. Apply it to all engineering work in this repo and in repos that install it.

## Read first

- [SKILL.md](SKILL.md) — the policy. Read it before changing behavior.
- [references/review-checklist.md](references/review-checklist.md) — before reviewing a diff.
- [references/architecture-guide.md](references/architecture-guide.md) — before choosing a structure.

## Repository rules

- Keep `SKILL.md` under 500 lines. Move detail into `references/`.
- Keep every reference one level deep from `SKILL.md`.
- Validate before committing: `python3 scripts/validate_skill.py .`
- Run `bash scripts/review_diff.sh` on the staged diff.
- Update `CHANGELOG.md` for user-visible changes.
- Do not add a reference file without a "Read when" row in `SKILL.md`.

## Non-negotiables

- Evidence over adjectives. Report what ran.
- Minimal diffs. No unrelated formatting.
- Security, tenancy, and error paths are part of correctness.
- AI-generated code is untrusted until verified.
