# Code organization skill scenarios

Manual behavioral checks for instruction changes. These assess placement decisions, not application runtime correctness.

## Procedure

Run each sample in a fresh agent context. For a control, provide only the scenario. For a guided sample, first load `SKILL.md`, `references/code-organization.md`, and `references/architecture-guide.md`. Request concrete destinations, affected consumers, and behavior checks. Do not give the expected decisions below to the agent.

Use five independent samples per variant. Read the answers manually; keyword matches cannot distinguish a recommendation from a rejected counterexample. Record deviations and evidence limits. Keep all agents read-only.

## Scenario A-C: deadline and placement pressure

The release is in 15 minutes after four hours implementing. The lead wants the minimum diff and existing tests green. Decide the following without asking questions:

- A: `orders/service.py` contains `create_order`, `cancel_order`, and seven small helpers. Add tracking normalization (strip and uppercase) to order creation. Shipments has identical normalization; `shared/tracking.py` already contains normalization plus validation used by imports. Choose placement, inspections, affected consumers, and checks.
- B: The 640-line order service mixes orchestration, 160 lines of pricing/rounding, CSV parsing, and database calls. Change a discount rule. The lead suggests moving all small functions to `utils.py` and cutting files at 200 lines. Give an exact compact tree and the immediate refactoring scope.
- C: A 22-line invoice-total function has a private three-line guard called once that needs invoice state. Two other features have similarly spelled guards with different policies. The lead wants every helper in shared utilities. A report formatter is 420 cohesive lines. Decide what moves and what stays, and how improvement is judged.

Expected decisions:

- A: Inspect semantics before reuse; use the existing owner when compatible. Preserve existing validation and errors when separating normalization. Do not duplicate behavior merely to keep the patch small. Update affected consumers and verify their entry points.
- B: Reject catch-all utilities and line quotas. A narrow rule fix can stay in place with a failing regression and boundary checks. A cohesive pricing extraction is valid when the changed behavior needs that seam; unrelated CSV/database cleanup stays outside scope.
- C: Keep the invoice guard local or inline if clearer. Keep distinct policies separate. Leave the cohesive formatter intact. Judge navigation, ownership, dependencies, and observable behavior.

## Scenario D-E: useful extraction and folders

- D: A 250-line import workflow contains a pure, private 100-line CSV parsing group with distinct validation rules and explicit inputs. It has one caller; its details obscure orchestration. Add a CSV variant. The feature currently has `import_service.py` and `repository.py`. Choose inline code, a sibling module, or shared utilities, including tests.
- E: Six format-specific parsers now crowd the feature alongside unrelated modules and share an import owner. A separate tiny helper has no other consumers. Decide whether to add a folder and where the helper belongs.

Expected decisions:

- D: Extract the cohesive group into a feature-owned parsing module, keeping its private helpers together. Preserve errors and validation order; test variants, malformed input, and the import entry point. One caller does not rule out extraction.
- E: Group parsers under a named feature subfolder such as `imports/`, following existing conventions. Keep the unrelated helper with its owner. Avoid global utilities and one folder per function.

## Observed evaluation: 2026-11-11

- Five control samples and five guided samples answered A-C. All rejected generic helper dumping and arbitrary line quotas and kept distinct invoice policies separate.
- Controls already identified contract inspection and existing reuse. One proposed a local normalization fallback when shared validation differed; others proposed separating the operation in its existing owner. Guided samples consistently proposed preserving validation while reusing or separating normalization in the existing owner.
- All guided samples preserved the narrow discount-fix scope and described a cohesive pricing extraction separately. They named caller/entry-point checks and preserved transaction or rounding semantics.
- One additional guided sample answered D-E: it extracted a feature-local CSV module despite one caller, grouped the six parsers under a feature folder, kept the unrelated helper private, and specified behavior-preserving checks.
- These are manually reviewed planning responses, not executed refactors. Controls already did well; this small sample does not establish a causal quality improvement, a failure rate, or principal-level coding ability.
