# Contributing

## Scope

This repository holds one skill. Changes should improve the policy, a reference, a script, or the packaging. Do not add project-specific rules that only make sense in one codebase.

## Workflow

1. Open an issue describing the failure mode the change addresses. "It reads better" is not a failure mode.
2. Make a small diff. One concern per pull request.
3. Run the checks:

```bash
python3 scripts/validate_skill.py .
bash scripts/review_diff.sh
```

4. Update `CHANGELOG.md` under `Unreleased`.
5. Describe observed evidence in the pull request: what you ran and what happened.

## Writing rules

- Short sentences. One idea per sentence.
- Active voice. Concrete verbs.
- No marketing adjectives. No "production-ready" without evidence.
- Every reference must be linked from `SKILL.md` with a "Read when" trigger.
- Keep `SKILL.md` under 500 lines.

## Adding a reference

1. Create `references/<topic>.md`.
2. Add a row to the reference table in `SKILL.md`.
3. Explain the trigger in the row: when should an agent load it?
4. Validate.

## Versioning

- MAJOR: a rule changes in a way that invalidates previous behavior.
- MINOR: a new reference, script, or policy section.
- PATCH: wording, links, typos.

## License

By contributing, you agree that your contribution is licensed under Apache-2.0.
