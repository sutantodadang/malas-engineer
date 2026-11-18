# Dependency Injection Contract — mechanically verifiable

**Language-independent rule:** injection is about explicitly providing and using side-effecting collaborators, not about class syntax. For pure computation, DI is not necessary. For functional, low-level and systems languages, a function argument, context struct, trait, callable, interface, or explicitly passed environment may be the idiomatic mechanism. See [universal application](universal-application.md).

## Four mandatory checks (where external collaborators exist)
1. **Declaration:** does the application behavior receive the external collaborator through constructor, explicit parameter, trait/callable/context, or framework injection?
2. **Storage/use:** does it retain (if needed) and actually call the supplied instance/function? No `NewRepository()`, `new PrismaClient()`, `SessionLocal()` or global DB lookup in the service.
3. **Production wiring:** does a composition/assembly boundary build actual effectful adapters and pass them to application behavior, then to input/presentation boundary if any?
4. **Test substitution:** can a fake/controlled collaborator be supplied through the same explicit boundary with no live network or DB?

If any check fails, injection is incomplete. Interfaces alone do not prove DI.

## Dependency graph
`main/bootstrap -> concrete PostgreSQLRepository -> Service(repository contract, external-client contract, clock) -> Handler(service)`
This is **construction order**. Runtime calls go `Handler -> Service -> repository/client`. Repository must not import service.

## Anti-patterns
- Service constructs repository: `NewService() { repo := NewPostgresRepo(...) }`.
- Service imports bootstrap container to resolve a collaborator: service locator.
- Global initialized DB connection read from service.
- Test only verifies a mock call but never verifies production wiring.
- Handler bypasses service for CRUD because it looks shorter.
- Interface added for every helper and every model, including pure functions.

## Interfaces where they help
- A service depends on external side effects or a collaborator whose behavior must be controlled in a unit test.
- A new implementation may need a different adapter or transaction strategy.
- In Go: define a narrow interface at consumer location; generated sqlc `Querier` may satisfy it. Avoid an adapter wrapper if it merely forwards calls.
- In Python: small Protocol or explicitly typed callable when useful; never make Java-style abstract base classes mandatory.
- In TypeScript: small structural contract or class constructor type for framework DI; do not instantiate ORM client inside service.

## Transaction and external call boundaries
For workflows spanning DB and HTTP, document transaction scope, retries, cancellation, idempotency and failure modes. Do not hold a DB transaction across long network calls by default. Do not hide a transaction inside a trivial forwarding wrapper.

## What the final report must prove
`DI: Service X receives Store Y and Client Z in constructor; production composition in file A; unit fake in test B.` Use actual inspected paths. If wiring was not checked, state NOT VERIFIED.
