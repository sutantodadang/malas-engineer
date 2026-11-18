# Universal application: any language, framework and paradigm

This is a **universal engineering skill**, not a Go/Python/TypeScript skill. The examples currently tested in those languages teach *contracts*, not exclusive support. Apply principles to every language and ecosystem, including languages not listed here.

## First classify the task

| Software shape | Explicit responsibilities (only when meaningful) | Do not force |
| --- | --- | --- |
| HTTP/RPC backend | transport handler -> application service/use case -> persistence/remote adapter; domain policy; assembly root | ORM wrappers that merely forward |
| Background job/consumer | event/queue adapter -> use case -> persistence/remote adapter | HTTP controllers |
| CLI / automation | argument/command parsing -> focused operation -> file/process/network I/O | five-layer folder trees for a tiny script |
| Frontend (web/desktop) | view/component -> state/application action -> domain rules -> API/storage adapters | repositories for visual-only components |
| Mobile app | screen/view -> presentation state -> use case (if warranted) -> platform/data adapter | one viewmodel/service per trivial gesture |
| Pure reusable library | public API -> cohesive domain modules -> optional effectful adapters | application controller or repository without I/O |
| Game/systems/embedded | input/event loop -> simulation/algorithm -> platform/IO boundaries | business-service classes with no benefit |
| SQL/migrations/IaC/config | named purpose, deterministic change, compatibility boundary, validation and rollback where applicable | pretending the artifact is an OO application |
| Functional program | pure core with effects at the edge; pass collaborators as functions/records | class/interface ceremony |

## Universal file-placement algorithm
1. Identify the unit of **responsibility** and its real reason to change, then the existing owner. Explain with a sentence: `This module owns X and changes when Y changes.`
2. Keep helper(s) with owner if they serve one cohesive purpose, lifecycle, and dependency set. Length and language are not split triggers.
3. Split if there are independently changing responsibilities, distinct effects/boundaries, separately testable policies, unrelated callers, or dependency cycles. Avoid one-file-per-function and monolithic catch-all modules.
4. Preserve established local naming, packages, module conventions, visibility and build tooling; don't import another language's architectural idioms automatically.
5. Prefer clear names (`invoice_service`, `payment_client`, `inventory_policy`) over `utils`, `manager`, `core2` when meaningful; no gratuitous directories.
6. Honor externally fixed file names or evaluator constraints; do not reorganize unrelated code.

## Dependency injection contract across paradigms
**The invariant is collaborator supply and use, not a `constructor` keyword.** For an effectful application behavior:
1. **Declare** exactly which side-effecting collaborators it needs through a constructor argument, function parameter, trait, callable, interface, protocol, environment passed explicitly, or framework DI token.
2. **Use** those exact supplied collaborators: no hidden `new DB()`, globals, service locator, or ignored injected member.
3. **Assemble** real collaborators at the proper lifetime boundary, including disposal/cancellation and request-scoped vs singleton concerns.
4. **Substitute** fake/in-memory adapters in an isolated test without live external infrastructure (when meaningful). For pure computations this gate is **not applicable**.

Paradigm examples, never mandatory templates:
- **Java/Kotlin/C#**: dependency-injected service class + constructor injection; container configuration in bootstrap; repositories/data adapters are optional when ORM itself provides a useful port.
- **Rust**: struct with injected trait bound or `Arc<dyn Trait>` when appropriate; borrow/ownership lifetimes correctly; avoid global clients.
- **Zig/C/C++**: pass explicit context structs, pointers/references, function tables or callable objects to effectful modules; never add OO ceremony just to use DI vocabulary.
- **PHP/Ruby/JavaScript**: framework/container injection or explicit constructor/function arguments; test with substitute collaborators.
- **Swift/Dart**: inject data clients through initializer/provider/constructor with platform lifetimes respected.
- **Elixir/Scala/Haskell/functional code**: pure core + effectful shell, pass effect handlers/functions or idiomatic module/behavior boundaries; avoid forcing service classes.
- **Shell/SQL/IaC**: isolate commands, external effects and state boundaries; prefer deterministic inputs, dry-run/testing where supported. DI may be **not applicable**.

## Default architecture selection
- Explicit layered architecture is the **preferred default for new nontrivial backend applications**, even in a language not named above.
- Choose analogous clear boundaries for other application types without imposing an HTTP stack.
- Prefer the repo's actual conventions for existing code; propose targeted refactoring rather than silent global restructuring.
- Not every feature needs domain objects, repository interfaces, services, DTOs, factories, or separate folders. Add each only with a concrete reason.

## Tests & proof must be stack-native
Use the actual project formatter, linter, type checker, test runner and build tools; inspect their configuration before inventing commands. Choose unit, integration and E2E tests based on behavior and risk. Verify the changed call graph, life cycle, failure cases and diff. Report what ran, what failed and what was not run. A successful Go/Python/TypeScript example is **not** evidence for untested languages or agent behavior.
