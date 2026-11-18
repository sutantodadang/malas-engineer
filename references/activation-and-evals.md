# Activation, mechanical checks, and reproducible behavior evaluation

## Activation reliability
The [installer](../README.md#quick-start) writes a short standing instruction to the agent’s native personal configuration. A manual skill-only copy uses on-demand discovery. Project rules and context limits affect both modes.

On Windows, two fresh Codex CLI 0.146.0 processes showed the standing rule and the installed entry point in `codex debug prompt-input`. Two fresh Claude Code 2.1.238 processes included both in requests captured by a local test endpoint. These probes used disposable user profiles and confirmed startup loading. The behavioral trials below measure task outcomes separately.

- Keep always-on instructions short and task-specific; do not paste a 1000-line manual into global settings.
- Use repository-local instructions for project-specific rules and exact test commands. Merge, do not overwrite.
- For critical flows, ask an agent to show the planned file placement and DI construction graph before edits.
- Automated checks and CI/test results outrank the agent's summary.

## Static architecture diagnostic
From a maintainer checkout:

`python3 scripts/architecture_audit.py /path/to/project --json`

This scanner uses Python AST for Python and text heuristics for Go/TypeScript. It is **not a complete architecture checker**. It can miss framework DI and indirect calls, and text heuristics may flag harmless code or miss genuine violations. Do not use `--fail-on-findings` as an automatic CI gate until reviewing expected alerts on your own repo. It never modifies code.

## Genuine model evaluation (requires actual coding agent runtime)
1. Start both runs from identical fresh repository worktrees with same prompt, tools, model and budget. Run one with no Malas Engineer, one with skill plus global instructions.
2. Ask each model to solve specific prompts from `evals/cases.json`; do **not** reveal rubric until grading.
3. Save output tree, git diff, tests executed, failing tests and agent's explanation. Do not use agent's self-reported tests as proof; run the commands yourself.
4. Grade 6 rubric dimensions 0/1/2, reject on critical failures. Run each case at least twice to evaluate variance.
5. Record false positives and manual edits needed. Change just the skill rules that caused failures, repeat evaluation with held-out cases.
6. Publish actual evidence, model version and environment before claiming compliance improvement.

Local examples and architecture diagnostic validate **code contracts**, not model compliance. `.artifacts/local-validation.json` explicitly labels these tests.
