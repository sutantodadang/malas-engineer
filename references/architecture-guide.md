# Architecture guide

Read this when choosing a structure, challenging a default, or reviewing a design.

## Stance

Architecture exists to keep the next change local and the test seams real. It is not a badge. A consistent existing style beats a partial migration to a better one.

The default for a new nontrivial backend is explicit layered architecture. The default is not a mandate. Scripts, tiny services, and existing codebases have their own correct answers.

## Selection ladder

Start at the top. Move down only when the context requires it.

| Level | Context | Shape | Cost |
|---|---|---|---|
| 0 | Script, CLI, one-file tool | Functions and modules | None |
| 1 | Small API, one team, under ~10 endpoints | Feature folders with handler and service inside | Low |
| 2 | Nontrivial backend, multi-domain, multi-tenant | Explicit layers per feature | Medium |
| 3 | Complex invariants, money, workflow, state machines | Add domain model and value types | Medium |
| 4 | Many small independent use cases | Vertical slices | Medium |
| 5 | Several transports or interchangeable stores | Ports and adapters | High |

Do not skip levels because a blog post did. Do not climb levels because a diagram looks professional.

## Layer contract

| Layer | Owns | Allowed imports | Forbidden |
|---|---|---|---|
| Handler | HTTP or RPC, parsing, boundary validation, auth context, response mapping | Service, transport DTOs | Repository, ORM, SQL, domain mutations |
| Service | Orchestration, policy, authorization, transaction boundary | Repository contract, domain, pure utilities | HTTP framework, driver-specific types |
| Repository | Queries, persistence mapping, tenant scope, composite operations | Database driver, generated query layer | HTTP responses, business policy |
| Domain | Entities, invariants, value objects, pure operations | Standard library, pure utilities | Framework, database, transport |
| Infrastructure | Adapters, clients, queues, caches, composition root | Everything it wires | Business rules |

Dependency arrows point inward. A handler may import a service. A service must not import a handler. A domain package must not import the database driver.

## Feature grouping versus layer grouping

**Layer grouping** is easiest for a small codebase with one domain.

```text
internal/
  handlers/
  services/
  repositories/
  domain/
```

**Feature grouping** is easier when the codebase has many domains.

```text
internal/
  booking/
    handler.go
    service.go
    repository.go
    domain.go
  billing/
    handler.go
    service.go
    repository.go
    domain.go
```

Either is acceptable. Do not mix both halfway. Pick one and keep it predictable. In feature grouping, keep the same layer names inside each feature so navigation stays uniform.

## Stack examples

### Go

```text
cmd/api/main.go                 # composition root
internal/booking/
  handler.go                    # HTTP
  service.go                    # workflow and policy
  repository.go                 # consumer-owned interface, if needed
  domain.go                     # invariants
internal/infrastructure/postgres/
  booking_repository.go         # adapter
```

Constructors return concrete types. Accept interfaces at the consumer boundary. Pass `context.Context`. Wrap errors with context. Do not panic on user input.

### TypeScript

```text
src/
  controllers/booking_controller.ts
  services/booking_service.ts
  domain/booking.ts
  repositories/booking_repository.ts        # contract
  infrastructure/db/booking_repository_pg.ts
  app.ts                                     # composition root
  tests/unit/booking_service.test.ts
```

### Django

```text
config/
  settings.py
app/
  domain/invoice.py
  services/reconciliation_service.py
  repositories/invoice_repository.py         # only for complex access
  models/                                    # Django ORM stays idiomatic
  views/reports.py                           # thin handlers
  urls.py
tests/
```

Django ORM is already an abstraction. Add a repository when it isolates complex queries or creates a meaningful test seam. Do not wrap every model.

### FastAPI

```text
app/
  routers/booking.py
  services/booking_service.py
  repositories/booking_repository.py
  domain/booking.py
  infrastructure/db.py
  main.py
```

## Variants

### Vertical slices

Use when features are mostly independent and change velocity matters more than shared domain modeling.

```text
features/
  create_booking/
    handler.py
    command.py
    repository.py
    tests.py
  cancel_booking/
    handler.py
    command.py
    repository.py
    tests.py
```

Keep cross-cutting domain rules and infrastructure explicit. Duplication between slices is acceptable when the shared abstraction would be speculative.

### Ports and adapters

Use when the same use case is reached through several transports, or when a store must be swappable.

```text
internal/booking/
  service.go          # use case
  port.go             # interface owned by the consumer
internal/adapters/http/
  booking_handler.go
internal/adapters/postgres/
  booking_repository.go
```

The port belongs to the consumer, not to the adapter. Do not create a port for a single implementation with no test seam.

## Anti-overengineering rules

Reject these unless the context proves otherwise:

- A repository for every table.
- An interface with one implementation and no test seam.
- A DTO that mirrors a struct field for field.
- An empty domain folder to satisfy a diagram.
- A generic base repository.
- A factory for a constructor with two arguments.
- A message queue for work that fits in one process.
- A microservice for a module that shares a transaction.
- A cache before a measured bottleneck.

## Existing codebases

1. Inspect the current conventions. Follow them for local changes.
2. Make the smallest change that fits.
3. If the code mixes concerns, explain the cost and propose staged refactoring.
4. Do not reorganize unrelated modules without approval.
5. If a migration is approved, write characterization tests first, then move one seam at a time.

## When to write an ADR

Write one when the decision:

- changes a public contract, schema, or dependency direction,
- selects a storage, messaging, or deployment model,
- accepts a known risk or constraint,
- reverses a previous decision.

Do not write an ADR for a naming choice or a local refactor. See `adr-template.md`.

## Review questions

1. Can a maintainer find the handler, the business rule, the persistence boundary, and the tests quickly?
2. Do dependency arrows point inward?
3. Does each layer own one kind of decision?
4. Is any layer present only to forward calls?
5. Would the next likely change touch one feature or five?
6. Can the risky behavior be tested without booting the whole system?
7. Is the design the smallest one that meets the known requirements?

## Further reading

- Google Engineering Practices, code review standard: https://google.github.io/eng-practices/review/reviewer/standard.html
- MADR decision records: https://adr.github.io/madr/
- The Twelve-Factor App: https://12factor.net/
- Go project layout, with the caveat that it is a community reference, not an official standard: https://github.com/golang-standards/project-layout
