# Architecture decision record template

Use MADR 4.0 style. One file per decision. Keep it short.

File name: `docs/adr/NNNN-short-title.md`

```markdown
---
status: "proposed | rejected | accepted | deprecated | superseded by ADR-NNNN"
date: YYYY-MM-DD
decision-makers: [names]
consulted: [names]
informed: [names]
---

# NNNN. Short title

## Context and problem statement

Describe the situation and the problem in two or three sentences. State the scope.
What forces are at play: constraints, quality attributes, deadlines, team size, existing contracts?

## Decision drivers

- Driver one
- Driver two

## Considered options

1. Option A
2. Option B
3. Option C

## Decision

State the chosen option in one sentence, then explain why.

## Consequences

### Positive

- What improves.

### Negative

- What gets worse or what risk is accepted.

### Neutral

- What changes without a clear win or loss.

## Pros and cons of the options

### Option A

- Good, because ...
- Bad, because ...

### Option B

- Good, because ...
- Bad, because ...

## More information

Links to the design doc, issue, benchmark, or prior ADR.
```

## When to write one

- A public contract, schema, or dependency direction changes.
- A storage, messaging, or deployment model is selected.
- A known risk or constraint is accepted.
- A previous decision is reversed.

## When not to write one

- Naming a variable.
- A local refactor with no contract change.
- A reversible experiment that fits in a branch.

## Review

An ADR is accepted when the decision-makers agree and the consequences are understood. Record dissent. Do not rewrite history: supersede an old ADR with a new one.

## Reference

- MADR: https://adr.github.io/madr/
