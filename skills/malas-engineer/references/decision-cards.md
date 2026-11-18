# Decision cards: file boundaries, ownership, and injection

Read this when creating or extracting code. Never substitute file size or number of functions for ownership.

## A. Decide where code goes (in this order)
1. **Transport?** Route registration, request/response mapping, HTTP-specific validation -> controller/handler. Authorization enforcement must not be bypassed by background/workers: enforce domain permission at application boundary too when required.
2. **Workflow?** Business rules involving decisions, multiple collaborators, transactions, orchestration -> service/use case.
3. **Persistence?** SQL, ORM queries, DB connection management, record mapping -> repository/SQLC adapter. For simple ORM backends, application service can depend on a deliberate ORM port; prefer repository when queries are complex or tests require substitutions.
4. **External integration?** HTTP client, payment provider, queue -> named client/adapter, not `repository` unless it is actually persistence.
5. **Pure reusable policy?** Computation with own business name and independent tests -> domain policy/module.
6. **Assembly?** Instantiate adapters, configure lifetimes and pass them into service/controller -> bootstrap/container/main.
7. **Private helper?** Same feature, owner, dependencies, and reason to change -> same file as owner. File placement is by responsibility, not length.

## B. Split or keep: observable decision table
| Scenario | Default | Why |
| --- | --- | --- |
| Service + DB connection setup in same file | SPLIT | Workflow and infrastructure have distinct ownership |
| Handler SQL + response JSON | SPLIT | Transport bypasses service/persistence boundary |
| `service.go` holds private `normalizeID` used only by service | KEEP | One small internal concern |
| CSV parsing algorithm has own failure modes, tests and reuse | SPLIT | Independently testable policy/adapter |
| Two workflows use different dependencies and change separately | SPLIT | Distinct reasons to change |
| Three tiny CRUD methods share a dependency and single business rule | KEEP | No independent cohesive module yet |
| 350-line service implements one cohesive workflow with local helpers | REVIEW | Length prompts inspection, never automatic split |
| 70-line file with request mapping, SQL and business decision | SPLIT | Layer violation regardless of size |
| Duplicate 5-line business validation in two features | REVIEW | Reuse only if semantics are exactly the same |
| SQLC Querier already implements needed port | KEEP DIRECT | A pass-through repository adds no value |
| 10 separate one-function classes with no state or boundary | MERGE | Anti-slop |
| Assignment requires functions in `Service.go` | HONOR CONSTRAINT | External contract outranks preferred file names |

**When unsure:** write one sentence: `This file owns X and changes when Y changes.` If two incompatible answers appear, separate; if two files have the same answer and one only forwards to the other, consider combining.

## C. Dependency injection proof (four pieces)
1. **Supply** through a constructor, parameter, closure or idiomatic framework boundary; never create a hidden DB/client inside application behavior. Pure computations mark DI not applicable.
2. **Usage** calls the injected collaborator; simply declaring an interface is not enough.
3. **Composition root** creates concrete adapters and provides them to the service and handler; only composition can know both interface and implementation.
4. **Test substitution** injects a fake/controlled adapter; test asserts actual calls/results without network/database.

### Bad
```python
class InvoiceService:
    def __init__(self, repo):
        self.repo = repo
    def create(self, invoice):
        return SqlInvoiceRepository().create(invoice)  # ignores injection
```

### Good
```python
class InvoiceService:
    def __init__(self, repo):
        self.repo = repo
    def create(self, invoice):
        self._validate(invoice)
        return self.repo.create(invoice)
```
The real adapter is constructed in bootstrap (not shown).

## D. Anti-layering illusions
- Moving DB code into `db_utils.py` but importing it from handlers does **not** create a valid service boundary.
- Naming a class `OrderRepository` does not make it persistence if it decides domain rules.
- Naming a function `get_service` does not prove DI if it creates a new DB connection on every call without lifecycle handling.
- Dependency injection is a runtime graph, not a folder structure.
- Unused interfaces and fake `Protocol` declarations are not architectural improvement.
- Two services calling each other cyclically is not clean layering. Extract genuine shared policy or change the dependency direction.

## E. Scope rules
On existing code, avoid forcing an unrelated system-wide architecture migration. For a requested new feature, keep explicit handler/service/persistence boundary where the feature needs them; preserve existing public API and files outside affected seam. For a user's explicit refactoring request, propose migration in slices with tests, do not silently break contracts.
