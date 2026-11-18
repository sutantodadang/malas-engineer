# File placement contract: decide, do not guess (all programming languages)

**Universal:** adapt the labels to the actual program. A UI event, CLI command, compiler pass or embedded loop may be the entry boundary instead of an HTTP handler. Do not invent a service layer where there is no meaningful orchestration. See [universal application](universal-application.md).

## Responsibility-to-file decision procedure
Ask these questions in order:
1. Is it transport boundary work? -> handler/controller/router module.
2. Is it orchestration, validation that involves domain policy, permission, workflow, or calling collaborators? -> service/use-case module.
3. Is it database or network I/O? -> repository or client adapter.
4. Is it pure reusable domain logic with independently meaningful rules? -> named domain policy/value module.
5. Is it assembly/configuration? -> composition root/configuration.
6. Is it a tiny private detail of one responsibility? -> keep private alongside its owner.

**If two responsibilities answer different questions above, split even if each is short.** This rule overrides minimizing file count.

## SPLIT if any strong indicator is present
- A service currently owns DB pool construction or HTTP response formatting.
- A file contains two independent workflows that use different dependencies and change separately.
- Distinct algorithm (retry backoff, CSV parser, pricing, reconciliation) has independent tests, reuse, or complexity obscuring service flow.
- A dedicated collaborator needs a separately replaceable failure boundary (external API vs repository).
- Cyclic import/cross-layer import reveals ownership confusion (redesign boundary rather than hiding cycle).

## KEEP together if all applicable
- Same feature, same reason to change, same dependency set and lifecycle.
- Short private guard, transform, or helper used only by this cohesive module.
- Splitting causes trivial forwarders, circular imports or repeated pass-through of internal state.
- A small file would carry no meaningful contract other than its filename.

## Examples
BAD: `handler.go` parses request, creates pgx pool, writes SQL, decides retry policy and writes response.
GOOD: `handler.go` -> `service.go` -> injected `BatchStore`; `postgres/batch_store.go` owns SQL; `retry_policy.go` only if independent named policy.

BAD: create `create_invoice_service.py`, `invoice_validator.py`, `invoice_helper.py`, `invoice_factory.py` for three field assignments.
GOOD: `invoice/service.py` for workflow and local guards, `invoice/repository.py` if queries/DB side effects need isolation.

BAD: add `shared/utils.py` for tenant authorization, formatting currency and CSV parsing.
GOOD: `tenant/access_policy.py`, `billing/money.py`, `imports/csv_parser.py` when each is independently cohesive; otherwise keep local helpers.

## When the task forces a particular file
Assignment's explicitly required names, signatures or file locations are higher priority than ideal architecture. Keep required public method(s) in that file; extract collaborators only if permitted and preserve the evaluator's expected API. Explain constraint, do not call the necessary compromise bad engineering.

## Placement proof before code
For each nontrivial file change, output in planning (not a lengthy essay):
`Responsibility | Destination | Why not existing file? | Imported dependencies | Test`
If a file is introduced solely to look architecturally layered, reject it.
