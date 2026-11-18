# Behavioral evaluation suite (language-independent, cross-language cases)

Use these scenarios to evaluate changes made by an agent. The [v5 release trials](reports/v5-trials.md) include replay instructions and independently graded outputs.

## Manual A/B protocol
1. Use fresh comparable branches or worktrees with the same code snapshot.
2. Run each prompt from `cases.json` on the same coding agent/model, once without the skill, once with both global instructions and skill installed; provide the same tools/time/budget.
3. Save final file tree, `git diff`, test commands/outputs and agent explanation for each run.
4. First mark each rubric dimension APPLICABLE or NOT APPLICABLE based on task, language and paradigm; for applicable checks grade 0=missing, 1=partial, 2=clear evidence. Architectural and DI critical failures reject only if the relevant behavior is applicable. A pure computation or SQL migration does not need a constructor or HTTP handler.
5. Compare number of manual interventions, boundary violations, runtime regressions, unnecessary files, and unsupported success claims. Repeat with at least two runs per case if possible.

Language coverage in `cases.json` includes multiple runtime paradigms beyond Go/Python/TypeScript; these are **prompts**, not executed agent evaluations. The JSON files are *ready-to-run prompts and grading criteria*, not benchmark results. Separate small subagent trials are documented in [the 2026-11-17 report](reports/2026-11-17-review.md); they do not establish results for the 33-case suite.

## Local contract tests vs model eval
Local `examples/` and `scripts/test_architecture_audit.py` execute actual code/negative samples, not agent tasks. Run the model eval separately with an authenticated coding-agent runtime and identical fresh worktrees. Record model name, revision, baseline/skill conditions, prompts, outputs and commands. Do not assign a model-compliance score from local tests.

## Replaying the small executable trial

Use `fixtures/agent-task/catalog.py` and the two prompts in `fixtures/agent-task/tasks.json`. Give each agent its own `fix/` and `review/` copy, then run `python3 evals/check_agent_trial.py PATH_TO_TRIAL` as an independent check. Run the agent's own test suite too. The checker tests observable outputs, exception behavior, unchanged API and read-only scope; review finding quality still needs source/report inspection. It is deliberately withheld from task agents.

For comparative claims, use neutral prompts that do not already prescribe architecture, fresh sessions, the same tools/model/budget, multiple trials and held-out tasks. Record unavailable token/latency data as unknown. Test activation separately with should-trigger and should-not-trigger prompts; explicitly passing a skill path does not test discovery. Compare existing skill, candidate, no-skill and a relevant competing workflow under equivalent conditions before claiming a win.
