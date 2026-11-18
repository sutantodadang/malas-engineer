# TypeScript explicit layers

Default: `controllers/book_controller.ts` (HTTP); `services/book_service.ts` (workflow); `repositories/book_repository.ts` (contract/adapter or a concrete abstraction); `bootstrap.ts`/`container.ts` (assembly), domain types and tests when needed. Framework convention may adapt folder names.

```ts
interface BookRepository { findById(id: string): Promise<Book | null>; }
class BookService {
  constructor(private readonly books: BookRepository) {}
  async get(id: string): Promise<Book> {
    const book = await this.books.findById(id);
    if (!book) throw new BookNotFoundError(id);
    return book;
  }
}
// composition root
const repo = new PrismaBookRepository(prisma);
const service = new BookService(repo);
const controller = new BookController(service);
```

Do not use `new PrismaClient()` inside BookService. Avoid framework-specific HTTP exceptions in services when they should be reused across transports; map domain errors in the controller. For NestJS, framework DI is acceptable if providers/tokens and production registration are demonstrably correct. Verify injection at runtime; interfaces disappear at TS runtime.

The user's `library-api` `BookService` constructor-injected repository is a useful preference reference, **not** a copy-paste gold standard: it imports `HttpException` and logs debug values. Improve those while keeping explicit layer navigation.
