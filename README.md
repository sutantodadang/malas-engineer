# Malas Engineer

> Be lazy about unnecessary work. Never be lazy about correctness.

An engineering quality gate for AI coding agents. It gives an agent a stable operating policy: how to choose an architecture, how small a diff should be, what to test, what to verify, and how to report evidence.

Version 4.0.0. Apache-2.0.

## Why

Coding agents are fast at producing plausible code and weak at knowing when it is wrong. Common failures repeat:

- Layers, interfaces, and wrappers that only forward calls.
- A rewrite when a surgical fix was enough.
- Tests that execute code but cannot detect a defect.
- Security and tenancy checks omitted on background paths.
- Confident summaries with no executed checks behind them.

This skill encodes the opposite habits.

## What is inside

| File | Purpose |
|---|---|
| `SKILL.md` | Core policy. Read first. |
| `references/architecture-guide.md` | Architecture selection ladder, layer contract, stack examples |
| `references/go-sqlc-pattern.md` | Go with sqlc, sqlx, and GORM; transactions; money types |
| `references/testing-guide.md` | Test selection, contract tests, property-based tests, mutation testing, flaky tests |
| `references/security-checklist.md` | AuthN/AuthZ, tenancy, input, secrets, dependencies, supply chain |
| `references/reliability-performance.md` | SLIs, SLOs, error budgets, latency budgets, load testing |
| `references/review-checklist.md` | Operational review checklist |
| `references/migration-guide.md` | Incremental adoption in an existing codebase |
| `references/ai-code-review.md` | Bug taxonomy for generated code and a verification protocol |
| `references/adr-template.md` | MADR decision record template |
| `references/agent-context-guide.md` | AGENTS.md, CLAUDE.md, and skill authoring rules |
| `scripts/validate_skill.py` | Frontmatter, structure, and link validation |
| `scripts/review_diff.sh` | Diff hygiene scan |

## Install

### Hermes

```bash
git clone https://github.com/sutantodadang/malas-engineer.git \
  ~/.hermes/skills/software-development/malas-engineer
```

Hermes discovers `SKILL.md` automatically.

### Claude Code

```bash
git clone https://github.com/sutantodadang/malas-engineer.git \
  ~/.claude/skills/malas-engineer
```

Use the repository as a project skill in `.claude/skills/`, or copy `CLAUDE.md` into the target repository root.

### Codex and other AGENTS.md readers

Copy `AGENTS.md` into the repository root, or reference this repository from an existing `AGENTS.md`.

### Any agent

The files are plain Markdown. Load `SKILL.md` and follow the reference triggers.

## Validate

```bash
python3 scripts/validate_skill.py .
bash scripts/review_diff.sh
```

The validator checks frontmatter fields, name rules, the 500-line limit, reference links, and orphan reference files.

## Design principles

1. **Smallest sufficient architecture.** Layers are a tool, not a badge.
2. **Evidence over confidence.** Observed, inferred, unknown.
3. **Minimal diff.** One concern per change.
4. **Risk-based tests.** Test at the level that can falsify the behavior.
5. **Secure by default.** Authorization, tenancy, and input handling are not optional.
6. **Progressive disclosure.** A lean `SKILL.md` routes to focused references.
7. **Plain language.** Short sentences, concrete verbs, no marketing.

## Compatibility

The skill follows the Agent Skills layout: `SKILL.md` with YAML frontmatter, optional `references/`, `scripts/`, and `assets/`. It works with Hermes, Claude Code, Codex, and any agent that reads Markdown instructions.

## Contributing

See `CONTRIBUTING.md`. Small, evidence-backed changes with a clear rationale are welcome.

## License

Apache License 2.0. See `LICENSE`.
