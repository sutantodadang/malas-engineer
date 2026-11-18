import { BookService, type Book, type BookReader } from "./service.ts";

class MemoryReader implements BookReader {
  private readonly books: Map<string, Book>;
  constructor(books: Map<string, Book>) { this.books = books; }
  async getById(id: string): Promise<Book | null> { return this.books.get(id) ?? null; }
}

export function createService(): BookService {
  const repository = new MemoryReader(new Map([["1", { id: "1", title: "Verified" }]]));
  return new BookService(repository);
}
