# Testing guide

Read this when planning tests, judging suite quality, or reviewing test code.

## Core rule

Test each behavior at the lowest level that can actually falsify it. A test that cannot fail when the behavior is wrong is not evidence.

## Selection matrix

| Change | Test level | What must be true |
|---|---|---|
| Pure function or rule | Unit | Boundaries, empty input, error paths |
| Bug fix | Regression unit or integration | Fails before the fix, passes after |
| Query, transaction, migration | Integration with real engine | Real SQL, real constraints, rollback |
| Service contract | Consumer-driven contract | Both sides verify the same contract |
| Serializer, parser, codec | Property-based | Round-trip or invariant holds |
| Authorization, tenancy | Negative integration | Wrong user, wrong tenant, wrong role rejected |
| Concurrency | Race detector plus repeated run | No data race, no deadlock, no lost update |
| Critical business logic | Mutation testing (targeted) | Mutants are killed |
| Hot path | Benchmark or load test | p95 and p99 within budget |
| Configuration, infrastructure | Smoke test | Boots and serves in a production-like environment |
| UI workflow | Few E2E tests | Critical journeys only |

## Pyramid, trophy, and the honest rule

The classic pyramid (many unit, fewer integration, few E2E) is a cost model, not a law. Integration tests with real dependencies became cheaper with containers. The testing trophy argues that integration tests catch the most real bugs per line for API code.

The rule that survives: put the test at the level where the failure can actually occur, and keep the suite fast enough that people run it.

| Level | Strength | Weakness |
|---|---|---|
| Unit | Fast, precise, cheap | Can miss wiring and SQL |
| Integration | Catches real boundaries | Slower, needs infrastructure |
| Contract | Cheap cross-service confidence | Does not test behavior inside a service |
| E2E | User-level confidence | Slow, flaky, expensive to maintain |

## Unit tests

- Test behavior, not implementation. Assert outputs and observable side effects.
- Cover boundaries: empty, nil, zero, one, maximum, malformed, unauthorized.
- Prefer sociable unit tests where collaborators are cheap. Mock at process or network boundaries, not at every internal function.
- One behavior per test. A test name should describe the behavior and the condition.
- Avoid asserting that a mock was called unless the call itself is the contract.

## Integration tests

- Use the real database engine, not an in-memory substitute with different semantics.
- Run migrations in the test setup. Test the schema the production code will see.
- Use Testcontainers or an equivalent to start dependencies close to production.
- Isolate state per test: transaction rollback, schema reset, or unique tenant.
- Test constraints, indexes that matter, and tenant scope.
- Keep integration tests in a separate suite so the fast unit loop stays fast.

## Contract tests

Use when two services or a client and server deploy independently.

- Consumer-driven contracts (Pact or equivalent) record what the consumer needs.
- The provider verifies the contract in its own pipeline.
- Schema tests validate OpenAPI or GraphQL output against the published schema.
- Negative contract tests: a field that must not be returned, a role that must be rejected.
- Contract tests do not replace integration tests inside a service.

## Property-based tests

Use for parsers, serializers, encoders, validators, and data transformations.

Properties to look for:

- Round-trip: `decode(encode(x)) == x`.
- Preservation: `sort(xs)` is a permutation of `xs`.
- Invariant: a total is never negative; a balance never exceeds its inputs.
- Idempotence: applying the operation twice equals applying it once.
- Equivalence: optimized path equals the reference path.

Practice:

- Let the framework generate inputs and shrink failures.
- Derandomize in CI so failures reproduce.
- Bound the number of examples per run.
- Combine with mutation testing on high-risk modules.

Common tools: Hypothesis (Python), fast-check (TypeScript), proptest (Rust), rapid (Go), jqwik (Java).

## Mutation testing

Mutation testing measures whether the suite detects defects. Coverage only proves code ran.

When it pays off:

1. The module has a precise correctness contract.
2. The suite is deterministic and reasonably fast.
3. Real bugs in that module resemble the mutations the tool creates.

Where to use it:

- Money, authorization, tenancy, state machines, parsers.
- Diff-based runs on changed code in pull requests.
- Nightly full run on critical modules.

Targets are context-dependent. Track the trend, not a universal number. Investigate surviving mutants in critical paths.

Common tools: Stryker (JS/TS/C#/Scala), PIT (Java), mutmut or Cosmic Ray (Python), go-mutesting (Go).

## End-to-end tests

- Cover a small number of critical user journeys.
- Prefer stable selectors and explicit waits over sleeps.
- Run against a production-like environment.
- Quarantine flaky tests instead of retrying blindly.

## Flaky tests

A flaky test is a defect in the suite.

1. Quarantine it. Do not let it block unrelated work.
2. Record the failure signature and the suspected cause.
3. Fix or delete it within an agreed window. A permanently skipped test is dead weight.
4. Never add retries to hide nondeterminism. Retries are acceptable only for known external instability, with a visible count.

## Test data

- Use builders or factories with sensible defaults.
- Do not share mutable fixtures across tests.
- Inject time and randomness. Do not call the wall clock directly in domain logic.
- Use unique identifiers per test to avoid cross-test coupling.

## Coverage

- Line coverage is a floor for finding untested code, not a goal.
- Branch coverage is more informative than line coverage.
- Mutation score is the honest measure of suite strength for critical modules.
- Do not add tests only to raise a number.

## Anti-patterns

- A test that asserts a mock was called and nothing else.
- A test that mirrors the implementation step by step.
- Snapshot tests accepted without reading the diff.
- Sleep-based synchronization.
- Shared database state between tests without isolation.
- Testing framework internals or trivial getters.
- A regression test that passes before the fix.

## CI order

1. Format and lint.
2. Type check or compile.
3. Unit tests.
4. Integration tests.
5. Contract tests.
6. E2E tests for affected journeys.
7. Security scans: SAST, dependency audit, secret scan.
8. Build and artifact provenance.

Fail fast. Report the exact command and the observed result.

## Further reading

- Martin Fowler, Test Pyramid: https://martinfowler.com/bliki/TestPyramid.html
- Pact contract testing: https://docs.pact.io/
- Testcontainers: https://testcontainers.com/
- Hypothesis: https://hypothesis.readthedocs.io/
