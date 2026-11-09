---
name: malas-engineer
description: "Engineering quality gate for coding agents. Use when designing, implementing, debugging, refactoring, reviewing, or testing code. Enforces explicit layered architecture for nontrivial backends, minimal diffs, risk-based tests, secure defaults, evidence-based verification, and plain technical English."
license: Apache-2.0
metadata:
  version: "4.0.0"
  author: Dadang Sutanto
  repository: "https://github.com/sutantodadang/malas-engineer"
  tags: "engineering, architecture, code-review, testing, security, go, sqlc"
---

# Malas Engineer

Be lazy about unnecessary work. Never be lazy about correctness.

This skill is a working policy, not a style essay. Load it for any engineering task: design, implementation, debugging, refactoring, review, testing, or documentation that changes behavior.

## How to use this skill

Read this file first. Load a reference only when its trigger applies. Do not preload every reference.

| Read when | Reference |
|---|---|
| Choosing or challenging an architecture | [references/architecture-guide.md](references/architecture-guide.md) |
| Go with sqlc, sqlx, or GORM | [references/go-sqlc-pattern.md](references/go-sqlc-pattern.md) |
| Planning tests or judging test quality | [references/testing-guide.md](references/testing-guide.md) |
| Auth, tenancy, input, secrets, dependencies | [references/security-checklist.md](references/security-checklist.md) |
| Latency, SLOs, load, capacity | [references/reliability-performance.md](references/reliability-performance.md) |
| Reviewing a diff or preparing a PR | [references/review-checklist.md](references/review-checklist.md) |
| Adopting this skill in an existing repo | [references/migration-guide.md](references/migration-guide.md) |
| Code was generated or assisted by an LLM | [references/ai-code-review.md](references/ai-code-review.md) |
| Writing an architecture decision record | [references/adr-template.md](references/adr-template.md) |
| Writing AGENTS.md, CLAUDE.md, or another skill | [references/agent-context-guide.md](references/agent-context-guide.md) |

## Priority order

1. Higher-priority instructions, user requirements, and safety rules.
2. Correct existing behavior and public contracts, unless the task changes them.
3. Facts from code, tests, logs, and version-accurate documentation.
4. The smallest change that stays readable, testable, and maintainable.
5. Evidence. Report what you ran. Never claim what you did not verify.

When these conflict, correctness wins over elegance. A clear explicit duplication beats a misleading abstraction.

## The loop

1. **Frame.** State the problem and acceptance criteria in one or two sentences. Name what is out of scope.
2. **Read.** Inspect the touched paths, callers, tests, schema, and conventions before editing. Find the root cause of a bug; do not patch the symptom.
3. **Decide.** Pick the smallest design that keeps the change local. Record real trade-offs. If a decision changes a public contract or an architectural boundary, write an ADR.
4. **Change.** Make a surgical diff. Preserve unrelated behavior, formatting, and dependencies.
5. **Verify.** Run the narrowest check that can falsify the change, then widen by risk. Use the evidence ledger below.
6. **Report.** Changed, verified, not verified. No adjectives.

For small tasks, run the loop silently and briefly. For high-risk tasks, write the trade-offs and the verification gaps down.

## Architecture: choose the smallest sufficient shape

Explicit layers are the default for a new nontrivial backend. They are not a universal template.

| Context | Default shape | Notes |
|---|---|---|
| Script, CLI, one-file tool | Plain functions or a few modules | Do not invent layers |
| Small API, one team | Feature folders; handler and service inside each feature | Add a repository only for nontrivial queries |
| Nontrivial backend, multi-domain | Explicit layers per feature: handler -> service -> repository -> domain | The default in this skill |
| Complex invariants, money, workflow | Add a domain layer and value types | DDD concepts only where they earn their place |
| Many small independent use cases | Vertical slices | Keep shared domain and infrastructure explicit |
| Several transports (HTTP, CLI, queue) | Ports and adapters | The port belongs to the consumer |

**Rule:** choose the shape that keeps the next change local and the test seams real. A consistent existing style beats a partial migration to a better one.

### Layer contract

| Layer | Owns | Must not |
|---|---|---|
| Handler / controller / view | Transport, parsing, boundary validation, auth context, response mapping | Business workflows, SQL, ORM queries |
| Service / use case | Orchestration, policy, authorization decisions, transaction boundary | HTTP framework types, driver-specific types |
| Repository / data access | Queries, persistence mapping, tenant scope, composite operations | Business policy, HTTP responses |
| Domain | Entities, invariants, value objects, pure operations | Framework, database, or transport imports |
| Infrastructure | Adapters, clients, queues, caches, composition root | Business rules |

Dependency arrows point inward. A handler may import a service. A service must not import a handler. A domain package must not import the database driver.

### Naming and placement

Use names a new maintainer can guess: `handler`, `service`, `repository`, `domain`, `infrastructure`, `tests`. Idiomatic alternatives are fine: `views` in Django, `handlers` in Go, `routes` in FastAPI. Group by feature when the codebase is large; keep the same layer names inside each feature.

If a maintainer cannot point to the handler, the business rule, the persistence boundary, and the tests in under a minute, the design is incomplete.

### When to stop adding structure

Stop when the next layer would only forward a call, rename an existing method, or satisfy a diagram. No per-table repositories, no empty domain folders, no interface with one implementation and no test seam, no DTO that mirrors a struct field for field.

## Change discipline

- Read before write. Inspect callers, tests, migrations, and configuration that the change touches.
- One concern per change. Do not mix refactoring, formatting, and behavior in one diff.
- Preserve public APIs, schemas, error contracts, and configuration unless the task changes them.
- Prefer existing utilities and patterns. Do not add a dependency for a few lines of code.
- Do not swallow errors, ignore return values, add catch-all fallbacks, or leave placeholder implementations presented as complete.
- Do not weaken or delete tests to make a change pass.
- Never commit secrets. Never run destructive commands without explicit scope and approval.

## Security defaults

These are non-negotiable on any changed path:

- Authenticate at the edge. Authorize per object and per function on the server. Authentication is not authorization.
- Enforce tenant scope in every query, including background jobs, exports, reports, and webhooks.
- Validate untrusted input at the boundary. Parameterize queries. Encode output for its context.
- Keep secrets out of code, logs, errors, and client responses. Use a secret manager and rotation.
- Fail closed. Do not return stack traces or internal identifiers to clients.
- Treat new dependencies as attack surface: necessity, maintenance, pinning, provenance.
- Add rate limits and abuse controls on authentication, recovery, and expensive endpoints.
- Log security events without sensitive content.

Read [references/security-checklist.md](references/security-checklist.md) before touching auth, tenancy, payments, file upload, or external integrations.

## Testing

Test each behavior at the lowest level that can actually falsify it.

| Change | Minimum evidence |
|---|---|
| Pure logic | Unit tests, including boundaries and error paths |
| Bug fix | A regression test that fails before the fix, then passes |
| Database query or transaction | Integration test against the real engine |
| Service-to-service contract | Consumer-driven contract test |
| Authorization or tenancy | Negative tests: wrong user, wrong tenant, wrong role |
| Concurrency | Race detector plus a repeated or stress run |
| Migration | Before/after comparison job plus a rollback drill |
| Hot path | Benchmark or load test with p95 and p99 |
| Configuration or infrastructure | Smoke test in an environment that mirrors production |

Line coverage is a floor, not a goal. For critical modules, mutation score is the honest measure of suite strength. A test that asserts a mock was called has not tested behavior.

Read [references/testing-guide.md](references/testing-guide.md) for selection, contract tests, property-based tests, mutation testing, and flaky-test policy.

## Reliability and performance

- Define SLIs as ratios of good events to valid events. Set an SLO target and a window. The error budget is the allowed violation.
- Measure before optimizing. Report p50, p95, and p99, not an average.
- Budget latency per hop. A request budget belongs to the caller.
- Bound every queue, pool, retry, and loop over user-controlled data.
- Use timeouts everywhere. Retry only idempotent operations, with jitter and a cap.
- Make background jobs idempotent and safe to replay.
- Watch for N+1 queries, unbounded scans, and work done inside a transaction that does not need it.
- Roll out with canaries or flags when the blast radius is real.

Read [references/reliability-performance.md](references/reliability-performance.md) before changing a hot path, a queue consumer, or a capacity-sensitive service.

## AI-generated code protocol

LLM output is a draft with a known bug distribution. Verify it as untrusted code.

The eight categories observed in the literature: functional and semantic bugs, reliability and performance bugs, syntax bugs, style and standards issues, hallucinated APIs or objects, system and memory bugs, test bugs, and unspecified defects.

Minimum checks for any generated change:

1. Does every referenced symbol, method, package, and version exist at that exact version?
2. Does the code handle empty, nil, zero, maximum, malformed, and unauthorized inputs?
3. Do the tests fail when the code is broken? Are the assertions real?
4. Are error paths, cancellations, and cleanup handled?
5. Does the diff contain unrelated edits or invented requirements?
6. Was the behavior reproduced, or only read?

Read [references/ai-code-review.md](references/ai-code-review.md) for the full checklist and prompt-side mitigations.

## Review protocol

Use severity labels so authors can act:

- `blocker:` correctness, security, data loss, or broken build.
- `major:` contract risk, maintainability, missing tests for a risky path.
- `minor:` clarity, naming, duplication.
- `nit:` style, optional.
- `question:` needs an answer before approval.
- `praise:` specific good work. Use sparingly.

Two independent passes:

**Pass A, correctness and design.** Compare against acceptance criteria. Read the final code as a maintainer. Check branches, error paths, contracts, and realistic growth risks.

**Pass B, diff hygiene.** Inspect `git diff` and `git diff --check`. Look for unrelated edits, debug logs, secrets, generated artifacts, accidental formatting, and missing call-site updates.

Then ask: what would break this? Try to construct one counterexample. Fix real issues and rerun the affected checks.

## Evidence ledger

Report in three buckets:

```text
Observed:  commands run, outputs seen, files changed
Inferred:  conclusions that follow from observed evidence
Unknown:   what was not checked, and why
```

Never turn an inference into an observation. Never report a planned check as a completed check.

## Commits and pull requests

- One logical change per commit. Do not mix refactoring, formatting, and behavior.
- Use Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`. Add a scope when it helps: `fix(auth): reject expired refresh token`.
- The subject states the behavior change, not the file touched.
- The body explains why, and records the verification commands and results.
- A pull request states: problem, approach, risk, verification, and rollback for data changes.
- Keep pull requests small enough to review in one sitting. If it cannot be reviewed, split it.

## Definition of done

- [ ] Acceptance criteria are met.
- [ ] The diff contains only related changes.
- [ ] Tests cover the changed behavior and the regression case.
- [ ] Lint, type check, and build pass, or the gap is reported.
- [ ] Security, tenancy, and error paths were considered on touched code.
- [ ] Public contracts and migrations are compatible, or the break is explicit.
- [ ] The change is readable without a walkthrough.
- [ ] Verification evidence is recorded.
- [ ] Remaining risks and unknowns are stated.

## Anti-patterns

- A layer, interface, or abstraction that only forwards a call.
- A generic repository for every table.
- A rewrite when a surgical fix is enough.
- A test that mirrors the implementation instead of the behavior.
- A cache, queue, or microservice added without a measured bottleneck.
- A comment that narrates syntax instead of explaining a decision.
- A summary that claims "production-ready" or "fully tested" without evidence.

## Technical English

Use short, direct sentences. One idea per sentence. Active voice. One name for one concept. Prefer concrete verbs: validate, read, write, return, reject, retry. State conditions and errors explicitly. Define uncommon abbreviations on first use.

This is ASD-STE100-inspired, not certified ASD-STE100.

## Final response contract

For engineering work, report:

1. **Changed:** behavior and files.
2. **Verified:** commands run and observed results.
3. **Not verified / risks:** gaps, unknowns, remaining failures.

Omit empty sections. Keep it short.
