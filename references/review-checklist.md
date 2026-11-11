# Review checklist

Use this proportionately. It is a thinking aid, not a reason to expand scope.

## Before reading the diff

- [ ] I know the requested behavior and acceptance criteria.
- [ ] I know which paths, contracts, and data the change touches.
- [ ] I know the risk level: auth, money, tenancy, migration, concurrency, or routine.
- [ ] I know what the author verified, and what they did not.

## Pass A: correctness and design

### Behavior

- [ ] The change does what the task asked, and only that.
- [ ] Edge cases are handled: empty, nil, zero, maximum, malformed, unauthorized.
- [ ] Error paths return the right error and do not swallow it.
- [ ] Concurrency, transactions, and ordering are correct where relevant.
- [ ] The change is backward compatible, or the break is explicit and planned.

### Design

- [ ] The change belongs in this layer.
- [ ] Dependency arrows still point inward.
- [ ] No layer exists only to forward a call.
- [ ] The abstraction is justified by a real boundary or test seam.
- [ ] The next likely change stays local.
- [ ] The design is no more complex than the problem.
- [ ] Data states, units, mutation, and resource ownership are explicit where relevant.
- [ ] Existing reuse candidates were inspected for matching contracts, not just matching names.
- [ ] Business policy stays with its feature or domain; shared utilities contain compatible mechanics.
- [ ] Each new module has a named responsibility and a valid dependency direction.

### Readability

- [ ] Names describe domain meaning, not implementation detail.
- [ ] Functions are cohesive and short enough to hold in mind.
- [ ] Control flow is direct. Nesting is limited.
- [ ] Comments explain why, not what.
- [ ] A new maintainer could follow the primary path without a walkthrough.
- [ ] Helper placement keeps the workflow readable: cohesive detail is extracted, tiny private detail stays local when that is clearer.
- [ ] File splits follow responsibilities, not line quotas or a one-function-per-file rule.
- [ ] Folders group related modules; no generic dumping ground or empty scaffolding was added.

### Tests

- [ ] Tests cover the changed behavior and the regression case.
- [ ] The tests would fail if the behavior were wrong.
- [ ] Assertions check outcomes, not mock calls alone.
- [ ] Integration tests use real boundaries where the risk is there.
- [ ] No test was weakened or deleted to make the change pass.

### Security and reliability

- [ ] Authorization and tenant scope are enforced on every changed path.
- [ ] Input is validated at the boundary.
- [ ] Secrets and sensitive data are not logged.
- [ ] Timeouts, retries, idempotency, and cleanup are handled.
- [ ] The change does not introduce an unbounded resource.

### Performance and scale

- [ ] No N+1 query on the changed path.
- [ ] Queries are paginated or bounded.
- [ ] No expensive work inside a transaction that does not need it.
- [ ] Performance claims are backed by a measurement.

## Pass B: diff hygiene

- [ ] `git diff` contains only related changes.
- [ ] No unrelated formatting or whitespace churn.
- [ ] No debug logs, commented-out code, or temporary files.
- [ ] No secrets, tokens, or credentials.
- [ ] No generated artifacts committed by accident.
- [ ] No new dependency without justification.
- [ ] Call sites, imports, configuration, and docs are updated.
- [ ] Moved code preserves public exports, error behavior, evaluation order, transactions, and cleanup.
- [ ] Migrations are reversible or have a documented rollback.
- [ ] `git diff --check` passes.

## Adversarial pass

Try to break it:

- What input makes this wrong?
- What caller did the author not consider?
- What happens on timeout, cancellation, or partial failure?
- What happens when the same operation runs twice?
- What happens with two concurrent requests?
- What happens at 10x the expected volume?
- What happens when the downstream dependency is slow or down?
- Can a lower-privilege user reach this?
- Can tenant A see tenant B?

If you find a real issue, fix it or request a fix, then rerun the affected checks.

## Severity labels

| Label | Meaning | Merge? |
|---|---|---|
| `blocker:` | Correctness, security, data loss, broken build | No |
| `major:` | Contract risk, maintainability, missing tests for a risky path | Discuss |
| `minor:` | Clarity, naming, duplication | Usually yes |
| `nit:` | Style, optional | Yes |
| `question:` | Needs an answer before approval | Hold |
| `praise:` | Specific good work | Yes |

## Evidence to request

- The exact commands run.
- The observed output.
- What was not run, and why.
- Any remaining risk.

Do not accept "tested locally" without the command and result. Do not accept "should work".

## Approval standard

Approve when the change improves the code health of the system and meets the acceptance criteria, even if it is not how you would have written it. Do not block on personal preference. Do block on correctness, security, and maintainability risks.

## Further reading

- Google Engineering Practices, What to look for: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Google Engineering Practices, The Standard: https://google.github.io/eng-practices/review/reviewer/standard.html
