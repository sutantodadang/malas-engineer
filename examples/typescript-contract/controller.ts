import { BookNotFound, BookService } from "./service.ts";

// An HTTP framework controller delegates to this transport mapper.
export async function bookResponse(service: BookService, id: string): Promise<{ status: number; body: object }> {
  try {
    const book = await service.getById(id);
    return { status: 200, body: book };
  } catch (error) {
    if (error instanceof BookNotFound) return { status: 404, body: { error: "not found" } };
    if (error instanceof Error && error.message === "id is required") return { status: 400, body: { error: "invalid id" } };
    throw error;
  }
}
