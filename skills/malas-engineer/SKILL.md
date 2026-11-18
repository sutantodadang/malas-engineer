---
name: malas-engineer
description: "Use when implementing, debugging, refactoring, reviewing, or testing code in any language, especially when deciding responsibility boundaries, dependency injection, file placement, or verification scope. Also applies to scripts, migrations, frontend and infrastructure."
license: Apache-2.0
---
# Malas Engineer

**Be lazy about unnecessary work, never about engineering quality.** Make the smallest complete change that a human can maintain.

## Select the task mode

User requirements and repository constraints win over stylistic defaults. Preserve existing public contracts and unrelated user edits. This skill applies to **all programming languages**; patterns depend on the actual runtime and paradigm.

| Task | Required behavior |
|---|---|
| Review or investigation only | Read, reproduce safely, and report findings. Do not apply fixes unless requested. |
| Small correction | Inspect the owner and callers, make the local edit, run the relevant check. Keep planning internal. |
| Feature or refactor across boundaries | Show a compact responsibility and test plan, implement the complete affected path, verify wiring and behavior. |
| Specification-driven task | Read the full source specification. Track each required and named optional/bonus item to an artifact and verification, or an explicit disposition; optional does not automatically mean implement. |

A layer with no meaningful responsibility is **not applicable**, not missing. Pure libraries, functional programs, SQL migrations and tiny scripts do not need invented controllers, repositories or class constructors. Map uncertain cases with [universal application](references/universal-application.md).

## Before editing

1. Read the actual entry point, affected behavior, callers, tests and relevant schema/build configuration. Search existing helpers before creating one.
2. Trace one real execution path: input/boundary -> core behavior -> effects, where present. Name actual files and mark relevant responsibilities present, missing or mixed.
3. Identify behavior, owner, consumers, side effects, failure modes and compatibility constraints. For changed responsibilities, choose `responsibility -> destination -> reason -> dependencies`. Keep cohesive private helpers with their owner.
4. For external dependencies, identify who constructs, supplies, uses and closes them. Constructor, function parameter, closure, trait or framework dependency injection must fit the language.
5. Choose the regression/contract test and applicable integration checks. Reproduce a bug before changing it when feasible. A simple copy or formatting edit does not require invented tests.

Do not turn this gate into a design document for every task. Ask a targeted question only when a missing fact would cause incompatible or unsafe work; otherwise state a reversible assumption and continue.

## Boundaries and dependency ownership

For **new nontrivial backends**, default to explicit handler/controller -> service/use case -> persistence/client boundaries. For existing code, improve only the seam needed for the requested behavior. For other software, map to its real presentation, workflow, domain and effect boundaries.

- **Transport/presentation:** decode inputs, validate boundary shape, obtain authentication context and map responses/errors. Delegate business workflows; no direct SQL/ORM in a layered handler.
- **Service/use case:** own application decisions, authorization and transaction policy. Receive external collaborators; do not construct DB pools, repositories, HTTP clients or hidden service locators. Keep reusable services free of transport-specific exceptions.
- **Adapters:** own queries, remote I/O and storage mapping; do not decide business policy. A remote client is not automatically a repository.
- **Domain:** isolate complex invariants when needed; do not scaffold an empty domain layer for CRUD.
- **Composition root / assembly boundary:** create actual external collaborators, supply them to consumers and own their lifetimes. Core behavior depends on small consumer-owned contracts where useful; assembly knows implementations. Avoid cycles and hidden mutable dependencies.

**Prove dependency injection through behavior:** the supplied collaborator is actually used, production construction supplies it, and a test can substitute it. Accepting an unused `repo` while calling a global database is fake injection. A fake-call assertion alone does not prove correct results or production wiring.

Interfaces are conditional, not a quota. Pure functions remain functions. Go SQLC queries may directly satisfy a small service-owned interface; do not invent generated signatures or forwarding repository wrappers. Read [dependency injection](references/dependency-injection-contract.md) when changing effectful collaborators.

## File placement

Use [decision cards](references/decision-cards.md) and [file placement](references/file-placement-contract.md) when a new file or extraction needs justification.

1. Put behavior in its owning boundary even if it is short.
2. Split distinct responsibilities with different reasons to change, dependencies or independently testable policies.
3. Keep tightly coupled private helpers together. Neither function length nor file length alone justifies a split.
4. Prefer cohesive feature modules. No empty layer folders, generic `utils/common/manager` dumps or one-file-per-function rule.
5. Extract shared behavior only after checking real consumers: inputs, validation order, errors, units, effects and authorization context must be compatible. Preserve necessary differences.

A maintainer should be able to locate input handling, business behavior, I/O and tests quickly. Use [code organization](references/code-organization.md) for borderline ownership/reuse decisions.

## Implementation and evidence

- Follow repository conventions. Touch the code, callers, tests, fixtures, exports, configuration and documentation actually required by the change; avoid unrelated rewrites or speculative abstractions.
- Validate trust boundaries, preserve error handling, parameterize queries, scope data access and protect secrets. Check cancellation/timeouts, resource lifetime, money/date semantics, transactions, retries and idempotency when affected.
- Anti-hallucination: inspect APIs and generated code. Mark material facts **VERIFIED**, **INFERRED** or **UNKNOWN** when the distinction matters. Never invent repository findings, output, requirements or passing tests.
- Test policies and outcomes; use integration tests for real persistence/network behavior and E2E for critical journeys when relevant. Include meaningful failure paths. Do not weaken assertions merely to get green.
- When two entry points promise equivalent behavior, run the same valid and invalid inputs through both. Vary any runtime default one path depends on, such as text encoding, locale or timezone. Check who owns resources after success and failure.
- Diagnose the first causal failure. Fix defects on the affected path and preserve unrelated edits.
- Keep technical writing plain and concise. No formal standards-conformance claim without its evidence.

## Completion gate

1. Compare the result with task acceptance criteria, including explicit file/signature constraints and disposition of named optional deliverables.
2. Inspect the full change, including newly created/untracked files. Trace the affected runtime path; check collaborator construction/use/lifetime **only where applicable**.
3. Challenge each new module and abstraction: does it own a distinct responsibility? Could combining it preserve cohesion? Are independent responsibilities still mixed?
4. Inspect relevant error/security/compatibility paths. Run configured checks appropriate to the change and record their actual exit/results. A successful command that discovered zero tests is not test coverage. Static diagnostics and `git diff --check` do not prove runtime correctness.
5. Report the outcome, meaningful changes, tests actually run and remaining risks. Mark unavailable checks **NOT RUN** with the observed reason. Distinguish completed implementation from unverified acceptance; do not imply release readiness from local examples.

For test choice and adversarial review, read [verification](references/verification.md). Once relevant checks pass, repeat only for new changes, failures or unresolved concerns.

## Conditional references

Read only the entries needed for the current task. Reference examples illustrate techniques; they do not prescribe a language or prove support for every stack.

| Trigger | Reference |
|---|---|
| Go / SQLC boundaries | [Go](references/go-sqlc.md), [detailed SQLC pattern](references/go-sqlc-pattern.md) |
| Python / TypeScript boundaries | [Python](references/python.md), [TypeScript](references/typescript.md) |
| Architecture tradeoff or major decision | [Architecture](references/architecture-guide.md), [ADR template](references/adr-template.md) |
| Migration or compatibility change | [Migration guide](references/migration-guide.md) |
| Test strategy or review depth | [Testing](references/testing-guide.md), [review checklist](references/review-checklist.md), [AI review pitfalls](references/ai-code-review.md) |
| Trust boundaries or reliability/performance risk | [Security](references/security-checklist.md), [reliability](references/reliability-performance.md) |
| Maintaining project instructions | [Agent context](references/agent-context-guide.md) |
