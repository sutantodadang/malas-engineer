# Contributing

## Scope

This repository holds one skill. Changes should improve the policy, a reference, a script, or the packaging. Do not add project-specific rules that only make sense in one codebase.

## Workflow

1. Describe the failure mode the change addresses. "It reads better" is not a failure mode.
2. Make a small diff. One concern per pull request.
3. Run the checks:

```bash
python3 scripts/build_installer.py --check
python3 scripts/validate_skill.py skills/malas-engineer
python3 scripts/validate.py .
npm ci --prefix examples/typescript-contract --ignore-scripts --no-audit --no-fund
python3 scripts/run_local_validation.py
bash scripts/review_diff.sh
```

The local runner writes results to `.artifacts/local-validation.json`. Historical reports in `evals/reports/` are preserved.

4. Update `CHANGELOG.md` under `Unreleased`.
5. Describe observed evidence in the pull request: what you ran and what happened.

## Writing rules

- Short sentences. One idea per sentence.
- Active voice. Concrete verbs.
- No marketing adjectives. No "production-ready" without evidence.
- References need a relevant read trigger; do not load the whole library on every task.
- Keep `SKILL.md` under 500 lines.

## Adding a reference

1. Create `skills/malas-engineer/references/<topic>.md`.
2. Add a row to the reference table in `skills/malas-engineer/SKILL.md`.
3. Explain the trigger in the row: when should an agent load it?
4. Validate.

## Shipping the installer

Edit the Markdown in `skills/malas-engineer/` or the installer source in `install/installer.py`. Run `python3 scripts/build_installer.py` and commit the resulting `install/malas-engineer.pyz` with its sources. The build includes the entry point, the license and only the reference files linked by the skill. CI reproduces the archive byte for byte and exercises installation in disposable profiles on Windows and Linux.

The public download follows the default branch. For an immutable download, replace `main` in the raw GitHub URL with the full commit SHA. Historical evaluations describe the revisions they tested.

## Versioning

- MAJOR: a rule changes in a way that invalidates previous behavior.
- MINOR: a new reference, script, or policy section.
- PATCH: wording, links, typos.

## License

By contributing, you agree that your contribution is licensed under Apache-2.0.
