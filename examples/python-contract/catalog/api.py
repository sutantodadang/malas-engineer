"""Transport adapter; map domain/application errors to status codes."""
from .service import BookNotFoundError, BookService

def get_book_response(service: BookService, book_id: str) -> tuple[int, dict]:
    try:
        book = service.get_book(book_id)
    except ValueError:
        return 400, {"error": "invalid book id"}
    except BookNotFoundError:
        return 404, {"error": "book not found"}
    return 200, {"id": book.id, "title": book.title}
