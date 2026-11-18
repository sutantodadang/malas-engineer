"""Application workflow. Do not import ORM or web framework here."""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Book:
    id: str
    title: str

class BookReader(Protocol):
    def get(self, book_id: str) -> Book | None: ...

class BookNotFoundError(Exception):
    pass

class BookService:
    def __init__(self, reader: BookReader) -> None:
        self.reader = reader

    def get_book(self, book_id: str) -> Book:
        if not book_id.strip():
            raise ValueError("book_id is required")
        book = self.reader.get(book_id)
        if book is None:
            raise BookNotFoundError(book_id)
        return book
