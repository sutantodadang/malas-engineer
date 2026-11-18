# Research synthesis — curated techniques, not copied instructions

Checked 2026-11-16. External sources support **techniques**, not promises that a model will obey. These references are used by topic; do not load this file for every short coding task.

## Release follow-up checked 2026-11-18

The v5 trials use independent outcome checks and retain the agent outputs so maintainers can rerun them. The comparison uses the published Superpowers verification workflow at a fixed revision. [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills) · [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/verification-before-completion/SKILL.md)

Comparing file and pipe input exposed a runtime dependency that ordinary unit tests missed. Python initializes standard input with configurable encoding and error handling. The release asks agents to exercise equivalent entry points on valid and malformed input under different defaults. The trial report distinguishes the example used for this edit from the later asynchronous task. [Python standard streams](https://docs.python.org/3/library/sys.html#sys.stdin) · [Release trials](../evals/reports/v5-trials.md)

## Follow-up comparison checked 2026-11-17

The following are inspected source documents, not head-to-head benchmark results. Their procedures serve different purposes, so feature counts and stars are not quality scores.

| Source | Useful practice | Application here |
| --- | --- | --- |
| [Agent Skills authoring guidance](https://agentskills.io/skill-creation/best-practices) | Moderate detail, conditional references, calibrated control | Reduce repeated universal-language/DI prose; retain concrete ownership decisions and route deeper details. |
| [Agent Skills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills) | Compare fresh runs with and without a skill; preserve artifacts, timing and grading | Isolated original/candidate/control tasks, independent acceptance checks, explicit unavailable telemetry. |
| [Anthropic skill-creator, pinned revision](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/skill-creator/SKILL.md) | Iterate outputs and separate description triggering from output quality | Actual coding/review artifacts; no activation claim from explicit skill invocation. |
| [Superpowers writing-skills, pinned revision](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/writing-skills/SKILL.md) | Pressure-test procedural instructions against a baseline | Repeated task agents, original snapshot and retained failures. A passing control does not demonstrate skill lift. |
| [gstack review, pinned revision](https://github.com/garrytan/gstack/blob/99256a8631d90c6d363408f037b87fbec1577890/review/SKILL.md) | Explicit completion evidence and inspection of actual callers | Inspect affected consumers and untracked output. Do not import its telemetry, tool dependencies or review-team ceremony into every small edit. |
| [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | Distinguish capability from regression tests; combine outcome checks with transcript review | Code acceptance tests plus manual report review; acknowledge easy-case ceiling and small sample. |

Positioning hypothesis: Malas Engineer can be useful as a compact engineering contract focused on file ownership, idiomatic dependency supply and honest completion. Superpowers is a broader workflow suite; gstack review is a specialized review workflow; skill-creator is an authoring/evaluation tool. Combining their useful ideas does not establish that this skill outperforms them. Require repeated held-out coding tasks, fewer regressions/manual corrections, and measured cost before making that claim.

## Skill authoring, activation and behavior testing
1. [Agent Skills specification](https://agentskills.io/specification): metadata, progressive disclosure, and portable references. Apply: keep master concise and attach focused examples.
2. [OpenAI Codex customization](https://learn.chatgpt.com/docs/customization/overview): always-on AGENTS guidance vs on-demand skill. Apply: two-level installation, not skill alone.
3. [OpenAI skill authoring guidance](https://learn.chatgpt.com/docs/learn/best-practices): begin with repeatable use cases and trigger descriptions. Apply: focus on handler/service/DI/split problems.
4. [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md): create/evaluate/revise loop. Apply: comparable task A/B harness and explicit scoring.
5. [Anthropic: test, measure and refine skills](https://claude.com/resources/articles/improving-skill-creator-test-measure-and-refine-agent-skills): distinction between triggering and successful output. Apply: measure both.
6. [Anthropic: Claude Code skills, hooks and rules](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more): reliable checks need hooks/tools, not just prose. Apply: optional deterministic diagnostic; do not claim prose guarantees.
7. [obra/superpowers](https://github.com/obra/superpowers): red-green-refactor, systematic debugging, verify-before-completion. Apply: tests that can fail and verification evidence.
8. [Google engineering small changes](https://github.com/google/eng-practices/blob/master/review/developer/small-cls.md): small self-contained CLs, avoid unrelated edits. Apply: impact and minimal diff gate.
9. [GitHub Copilot customization support](https://docs.github.com/en/copilot/reference/custom-instructions-support): instruction surfaces differ. Apply: keep installation provider-specific.

## Architecture, DI, readability and stack-specific boundaries
10. [Microsoft DI guidelines](https://learn.microsoft.com/dotnet/core/extensions/dependency-injection-guidelines): no direct construction within services, avoid service locator, mind lifetimes. Apply: four-part DI proof.
11. [Go Code Review Comments — Interfaces](https://github.com/golang/wiki/blob/master/CodeReviewComments.md): consumer-owned small interfaces. Apply: SQLC adapter satisfies narrow interface; no mock-everything.
12. [Effective Go](https://go.dev/doc/effective_go): naming and small idiomatic interfaces. Apply: avoid Java-style Go packages and `I*` interfaces by default.
13. [SQLC configuration](https://github.com/sqlc-dev/sqlc/blob/main/docs/reference/config.md): `emit_interface` emits a generated Querier when enabled. Apply: inspect config; don't assume it exists.
14. [FastAPI testing dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/): substitute external dependencies in test. Apply: verify framework wiring and fake injection.
15. [Google Testing Blog — Avoiding mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html): favor realistic fakes/high-fidelity tests. Apply: behavior checks beyond mock-call assertion.
16. [OWASP Go Secure Coding Practices](https://devguide.owasp.org/en/05-implementation/01-documentation/02-go-scp/): input, auth, logging, database safety. Apply: risk-based security acceptance checks.
17. [ADR templates based on Michael Nygard](https://github.com/architecture-decision-record/architecture-decision-record/blob/main/skills/architecture-decision-record-skill/reference/templates.md): record non-obvious tradeoffs for major decisions only, not one document per feature.

## User-provided style references (directly inspected excerpts, not blanket endorsements)
- [MNC transaction service](https://github.com/sutantodadang/mnc/blob/main/internal/app/transaction/service.go): constructor and repository-shaped dependency; tradeoffs include broad SQLC `Querier`, UUID MustParse panic risk, float conversion in money. Pattern to retain: explicit service and injected persistence; issue to avoid: unsafe input handling.
- [Library API book service](https://github.com/sutantodadang/library-api/blob/main/src/services/book_service.ts): constructor accepts book repository; tradeoffs: framework HTTP errors in service and debugging console logging. Pattern: explicit service/repository; avoid copying flaws.
- [Peruri coding test README / wiring](https://github.com/sutantodadang/peruri-coding-test): composition root constructs retry, repositories, service, handler; task may require particular file/signatures. Pattern: visible runtime graph and constraint-aware layer separation.
- [Indico](https://github.com/sutantodadang/indico): visible Go repository, `internal/`, `sqlc.yaml` from repo listing; inner call graph not fully inspected.
- [Widatech](https://github.com/sutantodadang/widatech) and [Wisata App](https://github.com/sutantodadang/wisata-app): public repository landing pages accessible but insufficient for definitive inner architecture classification. Do not make claims about individual layer boundaries without reading files.

## Not incorporated blindly
- Superpowers is an external workflow suite; we adapted evaluation, debugging, and verification concepts, not wholesale prompts.
- Mandatory TDD for literally every documentation/rename change would be wasteful; use regression-first when testable and risk based.
- A 100% test coverage mandate is misleading; test meaning and failures instead.
- DI **does not** mean one interface per class, nor one repository wrapper per SQLC query.
- No fixed maximum line count to decide module boundaries; responsibility and independent change drivers outrank length.
