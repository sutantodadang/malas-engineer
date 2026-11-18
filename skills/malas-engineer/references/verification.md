# Completion and adversarial review checklist

**Scope**: reviews remain read-only unless fixes are requested. Map specification deliverables to artifacts and checks; record the disposition of named optional items.
**Architecture**: trace the real input -> behavior -> effects path where these roles exist; no transport/persistence policy leaks or empty scaffolding. Pure functions do not need HTTP layers.
**DI**: supplied collaborators are used; assembly wires the real graph; substitution works in a unit test. Constructor, function or framework injection follows the project's paradigm; pure computations mark this N/A.
**Placement**: separate reason-to-change, dependencies or concerns -> separate file; private cohesive helpers remain together. Search for duplicate logic and catch-all helper modules.
**Correctness**: compare implementation to requested behavior and repository constraints; inspect negative, boundary, timeout, concurrent, tenancy, auth, error, idempotency cases where relevant.
**Testing**: unit for policy/service, integration for real DB/client/transactions, E2E for important user journeys. Run test commands and inspect actual result; report if unavailable. `git diff --check`, formatter, linter, type checker where configured.
**Maintainability**: meaningful names, no deep nesting or speculative abstractions, clear source of truth, minimal changes, no dead code.
**Final report**:
```
Change: [what and where]
Architecture: [actual affected path; collaborator wiring when applicable, otherwise N/A]
Split decisions: [why new modules exist / why helpers stayed]
Evidence: [commands and pass/fail/not run]
Risks: [unknowns or next steps]
```
Never convert an unrun test into PASS. Never claim a repo location was checked without opening it.
