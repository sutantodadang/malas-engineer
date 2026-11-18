# Malas Engineer v5.0.0

Malas Engineer helps coding agents decide where behavior belongs, who owns external resources, and which checks demonstrate that a change works. Small fixes stay with the owning module. New backends get explicit boundaries when the workflow needs them. Review requests stay read-only.

The same decisions apply to libraries, CLIs, migrations and frontends. The [task guide](references/universal-application.md) shows how to adapt them across languages.

## What this version actually tests

- **Go:** standard-library example builds and its `go test ./...` suite exercises injected fake, input failure, production composition.
- **Python:** `unittest` exercises injected fake, input errors, route mapping, production wiring.
- **TypeScript:** `tsc --noEmit` type-checks source and Node experimental type stripping executes tests for injected fake and wiring (does not replace testing under project-specific compiler/framework).
- **Architecture diagnostic:** unit tests verify that known bad samples are flagged and known good examples are not flagged. This is a *heuristic*, not a proof of all layered architecture claims.
- **Packaging:** metadata, reference links and 33 scenario definitions. The release ZIP contains a SHA-256 inventory of its files, excluding the inventory itself.

The [v5 trial report](evals/reports/v5-trials.md) compares actual agent changes on a Python CLI and an asynchronous JavaScript service. It includes replayable outputs, independent tests and a separate Codex discovery check. The [earlier trial](evals/reports/2026-11-17-review.md) covers Python library fixes and read-only reviews. Live databases, SQLC generation and customer deployments remain untested.

## Installation

Extract the `malas-engineer` directory from the release ZIP. The directory must contain `SKILL.md` directly. When updating an installation, preserve any personal customizations.

**Codex** uses `~/.agents/skills/malas-engineer`. For a team installation, use `.agents/skills/malas-engineer` in the project. Invoke `$malas-engineer` explicitly or let Codex select it from the task description. For a standing preference, merge [the Codex snippet](install/global-AGENTS.md) into your personal `~/.codex/AGENTS.md`.

**Claude Code** uses `~/.claude/skills/malas-engineer`. For a standing preference, merge [the Claude snippet](install/global-CLAUDE.md) into your existing `~/.claude/CLAUDE.md`.

**Hermes (where compatible):** place skill at `~/.hermes/skills/software-development/malas-engineer` as described by the existing Malas Engineer repository. This is skill discovery, not proof of always-on execution.

**Repo-local:** for team/project rules, add short repo-root `AGENTS.md` or `CLAUDE.md` with exact build/test commands. Skill internal `AGENTS.md`/`CLAUDE.md` are *for maintaining this skill repository*; the contents of `install/` are the snippets for global activation.

## Commands

```bash
python3 scripts/validate.py .
npm ci --prefix examples/typescript-contract --ignore-scripts --no-audit --no-fund
python3 scripts/run_local_validation.py
(cd scripts && python3 -m unittest -v test_architecture_audit)
(cd examples/go-contract && go test ./...)
(cd examples/python-contract && python3 -m unittest discover -s tests -v)
node examples/typescript-contract/node_modules/typescript/bin/tsc -p examples/typescript-contract/tsconfig.json
node --experimental-strip-types --test examples/typescript-contract/service.test.ts
python3 scripts/architecture_audit.py /path/to/your/repo --json
```

For architecture scans, review findings manually; textual Go/TypeScript patterns and Python AST have false positives/negatives. `--fail-on-findings` is opt-in.

## Content map

- `SKILL.md` — engineering contract, gate before and after editing
- `references/universal-application.md` — **apply to every language/paradigm**, with task-shape mapping and flexible DI
- `references/decision-cards.md` — **split vs keep** decisions and clear DI fail examples
- `references/dependency-injection-contract.md` — construction, actual usage, production wiring, fake substitution
- `references/file-placement-contract.md` — layer ownership and file movement
- `references/go-sqlc.md`, `python.md`, `typescript.md` — stack conventions
- `references/research-synthesis.md` — 17 public sources and user repository evidence
- `references/activation-and-evals.md` — always-on limitations and actual A/B steps
- `examples/` — running Go, Python and TypeScript demonstrations
- `scripts/architecture_audit.py` — diagnostic scanner, never changes files
- `evals/cases.json`, `evals/rubric.json` — **multi-language** model evaluation tasks, not benchmark scores
- `evals/reports/local-validation.json` — recorded local checks and their scope

The skill description should trigger on **coding tasks in any language**, but always-on `AGENTS.md`/`CLAUDE.md` is the durable pointer. Neither grants deterministic compliance without runtime checks and evaluation.

## Reproducing the evidence
`python3 scripts/run_local_validation.py` runs local checks and refreshes `evals/reports/local-validation.json`. Install the pinned example compiler first; Python, Go and Node must be available. CI is configured to run the same checks on Windows and Linux. The runner does not execute model trials. See `evals/` for separate agent evidence and the broader benchmark protocol.
