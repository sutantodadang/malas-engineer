# AI-generated code review

Read this when code was generated or assisted by a language model, or when reviewing an agent's pull request.

## Stance

Generated code is a draft with a known bug distribution. Treat it as untrusted until verified. Speed is not evidence.

A survey of 72 studies on bugs in AI-generated code groups the observed defects into eight categories:

| Category | What it looks like |
|---|---|
| Functional | Wrong business logic, semantic misunderstanding, incorrect algorithm |
| Reliability | Performance problems, instability, resource exhaustion |
| Syntax | Code that does not compile or parse |
| Style and standards | Inconsistent conventions, duplication, readability issues |
| Hallucination | Invented APIs, packages, methods, configuration keys, or versions |
| System | Memory errors, OS or network incompatibility, resource management |
| Test | Wrong assertions, tests that cannot fail, flaky or meaningless tests |
| Unspecified | Mixed causes or defects that do not fit the other groups |

Functional and semantic bugs are the most common and the hardest to see in review. Hallucinated APIs are the fastest to catch if you check.

## Verification protocol

Run this for every generated change, proportionately to risk.

### 1. Existence

- [ ] Every function, method, package, and configuration key exists at the version in use.
- [ ] Every version number is real and compatible.
- [ ] Imports resolve. No invented module path.
- [ ] The API signature matches the actual library, not a plausible one.

### 2. Behavior

- [ ] The code implements the requested behavior, not a plausible adjacent behavior.
- [ ] Business rules match the specification, including rounding, ordering, and defaults.
- [ ] The change does not add unrequested features.
- [ ] The change does not remove existing behavior silently.

### 3. Boundaries

- [ ] Empty, nil, zero, one, maximum, malformed, and unauthorized inputs.
- [ ] Unicode, long strings, large payloads, and unexpected types.
- [ ] Time zones, daylight saving, leap days, and clock skew.
- [ ] Pagination limits and collection bounds.

### 4. Failure

- [ ] Errors are propagated, wrapped, and classified.
- [ ] Timeouts, cancellation, and cleanup are handled.
- [ ] Partial failure does not leave inconsistent state.
- [ ] Retries are safe for the operation.

### 5. Concurrency

- [ ] Shared state is protected or absent.
- [ ] The same operation twice does not corrupt data.
- [ ] Locks have a consistent order.
- [ ] The race detector or an equivalent tool passes.

### 6. Security

- [ ] Authorization is enforced on the server, per object and per function.
- [ ] Tenant scope is applied.
- [ ] Input is validated and queries are parameterized.
- [ ] No secrets, tokens, or personal data in logs or errors.
- [ ] New dependencies are necessary and maintained.

### 7. Tests

- [ ] The tests fail when the behavior is wrong.
- [ ] Assertions check outcomes, not only that a mock was called.
- [ ] The test data represents real shapes.
- [ ] No test is skipped, weakened, or made order-dependent.
- [ ] The regression case exists for a bug fix.

### 8. Diff

- [ ] Only related files changed.
- [ ] No debug prints, commented-out code, or temporary files.
- [ ] No unrelated formatting.
- [ ] No invented requirement or acceptance criterion.

## Prompt-side mitigations

Better input reduces the defect rate:

- Provide the exact files and symbols in scope. Do not ask the model to guess the codebase.
- State the acceptance criteria and the non-goals.
- Give the commands to run and the expected output shape.
- Provide examples of the existing convention.
- Ask for a plan before a large change.
- Ask the model to list assumptions and unknowns.
- Require a verification section with commands and observed output.

## Review-side mitigations

- Review generated code with the same checklist as human code, plus the existence checks.
- Do not approve a large generated diff in one pass. Review by concern.
- Run the tests. Read the assertions.
- Run the linter and the type checker.
- For security, money, auth, tenancy, and migrations, require human review regardless of who generated the code.
- Prefer a small verified change over a large plausible one.

## Common failure patterns

| Pattern | Detection |
|---|---|
| Invented library method | Search the installed source or exact-version docs |
| Plausible but wrong SQL | Run against the real schema; check the query plan |
| Test that asserts a mock | Read the assertions |
| Happy-path-only logic | Ask for empty, error, and unauthorized cases |
| Duplicated helper | Search the codebase before accepting a new utility |
| Silent fallback | Search for `catch`, `except`, `if err != nil { return nil }` |
| Unbounded loop | Look for iteration over user-controlled collections |
| Fake success summary | Require commands and observed output |

## Reporting

Separate what you observed from what the model claimed. A generated summary is not evidence.

```text
Observed:  tests run, output, files changed
Inferred:  conclusions from the output
Unknown:   paths not exercised, dependencies not verified
```

## References

- A Survey of Bugs in AI-Generated Code: https://arxiv.org/abs/2512.05239
- Assessing the Quality and Security of AI-Generated Code: https://arxiv.org/abs/2508.14727
- OWASP Secure Code Review Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
