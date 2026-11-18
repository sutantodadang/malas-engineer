# Code organization

Read when adding a function, choosing where a helper belongs, extracting code, or splitting files and folders.

Optimize for a maintainer following a behavior from entry point to result. File count and function length are not quality scores. The goal is clear ownership with few unnecessary jumps.

## Before adding code

1. Read the entry point and its callers, tests, imports, and adjacent modules.
2. Search by behavior as well as name. Inspect existing helpers before adding another implementation.
3. State the new responsibility in one sentence. Identify its inputs, result, failures, side effects, and actual consumers.
4. Choose the narrowest owner using the table below. Check that its dependencies can point in the right direction.

Reuse requires compatible semantics: accepted inputs, normalization order, units, time zones, errors, mutation, and tenant or authorization context. Similar syntax does not prove a shared contract. Do not change existing callers' validation merely to reuse a helper.

## Placement decision

| Evidence | Placement | Example |
|---|---|---|
| A short operation is clearer inline and has no useful independent name | Keep inline | An obvious field assignment |
| A tiny helper explains one caller and depends on its local policy or state | Private helper near the caller | A guard on an invoice transition |
| A cohesive calculation, parser, or helper group obscures the main workflow or owns distinct rules | Named sibling module in the feature, even with one caller | `orders/pricing.py`, `orders/csv_import.py` |
| Several modules in one feature need the same behavior | Feature-owned module | `orders/validation.py` |
| Several features need the same business rule | Owning domain module with a narrow API | `billing/tax.py`, not `shared/utils.py` |
| Independent consumers need the same domain-neutral mechanics and agree on its contract | Existing shared module, or a narrowly named utility module | `shared/date_ranges.py` |
| Code depends on HTTP, a database, files, or a remote client | Its transport or infrastructure owner | A storage adapter, not a pure utility |

A function being small does not make it a utility. A function being pure does not make it domain-neutral. Keep discount, authorization, and tenant policy with their owners.

When an existing utility almost fits, identify the mismatch. Extract a common operation only if it has a coherent contract and preserves current consumers. Otherwise keep the distinct behavior with its owner. Do not add mode flags to make unrelated policies look reusable.

## When to split a file

Extract a cohesive responsibility when one or more of these are true:

- Reading a workflow requires scrolling past substantial parsing, formatting, or calculation detail.
- Groups of functions use different dependencies and change for different reasons.
- Testing a calculation requires setting up unrelated network or database infrastructure.
- Multiple callers need the same policy, but currently copy it or import a workflow module to reach it.
- A module's name no longer describes its contents without joining unrelated responsibilities with "and".

Name the responsibility first, then move the functions and private helpers that implement it together. Keep the public workflow readable at one level of detail. Keep the new API small and hide implementation helpers using the language's visibility conventions.

Keep code together when splitting would require readers to bounce through trivial forwarding functions, pass a large bundle of private state, or introduce cyclic imports. Revisit the proposed boundary instead of hiding a cycle with lazy imports or re-export files.

Hundreds of lines warrant inspection, not automatic splitting. A cohesive formatter can stay in one file. A much smaller module can still need splitting when it mixes unrelated policy and transport. Generated code follows its generator's layout.

## Folder boundaries

- Follow the repository's naming, packaging, and test-location conventions.
- Keep a feature flat while its modules remain easy to scan.
- Add a subfolder when a related group has a recognizable responsibility and ownership boundary, such as several import formats or storage adapters.
- Use names that predict contents. Avoid new catch-all `utils`, `helpers`, `common`, `misc`, or `manager` modules.
- Extend an existing utility only if the behavior fits its current responsibility. Do not reorganize an unrelated legacy folder for naming alone.
- Keep tests aligned with the owning behavior. Moving a function does not require exposing a private API just to test it.
- Avoid empty layers, one-folder-per-function scaffolding, and index/barrel files that expose every internal symbol.

## Example: pricing inside an order service

Suppose `orders/service.py` contains workflow orchestration, a cohesive group of pricing rules, CSV parsing, and persistence calls. The requested change adds a pricing calculation used by order creation and quotes.

First search for an existing pricing owner. If none exists, use:

```text
orders/
  service.py           # coordinates the order workflow
  pricing.py           # price, discount, rounding; private helpers stay here
  quotes.py            # calls the same pricing policy
tests/orders/
  test_pricing.py       # amounts, thresholds, rounding and rejected inputs
  test_service.py       # workflow still reaches the correct policy
  test_quotes.py        # quotes use the same contract
```

Move the pricing calculation and its cohesive helper group together. Pass the required values explicitly; do not make `pricing.py` import `service.py` or reach into request context. Preserve rounding order, error behavior, and the existing transaction boundary. Leave unrelated CSV and persistence reorganization outside this change.

For a narrow discount bug fix that does not require a new boundary, patch and verify the existing policy first. An urgent deadline does not justify adding another implementation. Extract only the seam needed for the requested behavior; propose larger cleanup separately.

Do not produce `utils.py` containing prices, CSV parsing, and authorization checks. Do not produce a separate file for every three-line price helper. Both layouts obscure who owns the calculation.

## Safe extraction procedure

1. Search all consumers, including public exports, dynamic registrations, fixtures, and tests.
2. Capture behavior at the current boundary with focused tests; include failures and boundary values. For a bug fix, demonstrate the regression before fixing it.
3. Identify what moves and what stays: policy, I/O, mutable state, resource lifetime, and transaction ownership.
4. Move a cohesive unit without changing its semantics. Keep movement and behavior changes distinguishable in the diff or separate commits when useful.
5. Update imports and consumers. Preserve public entry points when compatibility requires them; a temporary compatibility wrapper needs a stated removal condition.
6. Remove the superseded implementation. Check for stale references, import cycles, accidental exports, and changed evaluation order.
7. Run the affected tests and relevant import/build/type checks, including a real entry-point test. Read the final call path and confirm the move reduced conceptual clutter.

## Review evidence

For a nontrivial placement decision, a short note is enough:

```text
Owner: order pricing policy
Consumers: create_order and quote_order
Destination: orders/pricing.py; both workflows import it
Dependencies: values and domain types; no service or request imports
Checks: threshold/rounding/error cases plus order and quote entry points
```

Fill this from inspected code. Do not invent a second consumer or claim that the checks ran when they are only planned.

Before accepting the result, locate the entry point, policy, I/O, and tests. Verify that the primary path is easier to follow and that a likely change stays with its owner. If extraction only changed file counts, reconsider it.
