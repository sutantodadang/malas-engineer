import test from "node:test";
import assert from "node:assert/strict";
import { BookNotFound, BookService, type Book } from "./service.ts";
import { createService } from "./bootstrap.ts";

test("uses injected reader, not hidden ORM", async () => {
  let calls = 0;
  const fake = { async getById(_id: string): Promise<Book> { calls++; return { id: "x", title: "Injected" }; }};
  const book = await new BookService(fake).getById("x");
  assert.equal(book.title, "Injected");
  assert.equal(calls, 1);
});
test("invalid input skips repository", async () => {
  let calls = 0;
  const fake = { async getById(_id: string) { calls++; return null; }};
  await assert.rejects(() => new BookService(fake).getById(""), /required/);
  assert.equal(calls, 0);
});
test("composition root supplies a real adapter", async () => {
  assert.equal((await createService().getById("1")).title, "Verified");
  await assert.rejects(() => createService().getById("unknown"), BookNotFound);
});

import { bookResponse } from "./controller.ts";
test("transport maps application errors", async () => {
  assert.equal((await bookResponse(createService(), "1")).status, 200);
  assert.equal((await bookResponse(createService(), "nope")).status, 404);
  assert.equal((await bookResponse(createService(), " ")).status, 400);
});
