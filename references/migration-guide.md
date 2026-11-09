# Migration guide

Read this when adopting the skill in an existing repository, or when changing an architecture that is already in production.

## Principle

Do not rewrite a working system to satisfy a diagram. Adopt the parts of the skill that reduce real risk, one seam at a time.

## Adoption order

1. **Freeze conventions.** Write `AGENTS.md` with the commands, boundaries, and constraints an agent cannot guess.
2. **Add the fast checks.** Format, lint, type check, unit tests. Make them run in one command.
3. **Add review guardrails.** Use the checklist and severity labels. Do not add process that nobody follows.
4. **Pick one seam.** Choose the highest-pain module, not the whole codebase.
5. **Characterize behavior.** Write tests that capture current behavior before changing structure.
6. **Move one boundary.** Extract a service or repository behind a contract, with the old path still working.
7. **Verify with a parallel run.** Compare old and new outputs on the same inputs.
8. **Switch traffic.** Use a flag or canary. Keep a rollback.
9. **Repeat.** Only after the first seam is stable.

## Strangler fig pattern

```text
1. Route a small percentage of traffic to the new path.
2. Compare outputs. Log differences.
3. Increase traffic only when differences are understood.
4. Remove the old path after a stable period.
```

Do not run two write paths against the same data without an idempotency and reconciliation plan.

## Branch by abstraction

When a dependency or storage must change:

1. Introduce an interface at the consumer boundary.
2. Implement it with the existing behavior.
3. Switch callers to the interface with no behavior change.
4. Add the new implementation.
5. Switch implementation behind a flag.
6. Remove the old implementation.

This keeps every step reversible.

## Characterization tests

Before refactoring legacy code:

- Capture inputs and outputs from the current system.
- Assert the current behavior, including quirks you intend to keep.
- Mark behaviors you intend to change as explicit failing tests, not silent edits.
- Store fixtures that represent real payloads, sanitized.

## Database migrations

- Add nullable columns first.
- Backfill in bounded batches.
- Add constraints after the backfill is complete.
- Deploy code that can read both shapes.
- Remove the old shape only after the new code is stable.
- Test the rollback. A migration that cannot be reversed needs a documented forward fix.

## Parallel run

For a risky replacement:

```text
request -> old path -> result A
        -> new path -> result B
compare A and B, log differences, serve A until confidence is high
```

Compare on normalized values. Define what counts as a difference. Do not compare timestamps or identifiers that legitimately differ.

## Rollback

Every migration needs:

- a trigger condition,
- the exact rollback step,
- the data implication of rolling back,
- the person or automation that executes it.

## What not to do

- A big-bang rewrite with no parallel run.
- Moving files without tests.
- Renaming layers while changing behavior.
- Enforcing a new architecture on unrelated modules.
- Adding a framework to solve an organizational problem.
- Deleting the old path before the new one has survived a full business cycle.

## Measuring progress

Track:

- lead time for a change in the migrated area,
- defect rate in the migrated area,
- time to onboard a new maintainer,
- test runtime,
- number of unrelated files touched by a typical change.

If the migration does not improve one of these, stop and reassess.

## Further reading

- Martin Fowler, StranglerFigApplication: https://martinfowler.com/bliki/StranglerFigApplication.html
- Martin Fowler, BranchByAbstraction: https://martinfowler.com/bliki/BranchByAbstraction.html
- Google Engineering Practices: https://google.github.io/eng-practices/
