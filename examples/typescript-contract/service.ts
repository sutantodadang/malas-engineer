export type Book = { id: string; title: string };

// Consumer-side structural contract. No ORM client in application service.
export interface BookReader {
  getById(id: string): Promise<Book | null>;
}

export class BookNotFound extends Error {}

export class BookService {
  private readonly reader: BookReader;
  constructor(reader: BookReader) { this.reader = reader; }

  async getById(id: string): Promise<Book> {
    if (!id.trim()) throw new Error("id is required");
    const book = await this.reader.getById(id);
    if (book === null) throw new BookNotFound(id);
    return book;
  }
}
