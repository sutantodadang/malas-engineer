import unittest
from unittest.mock import Mock

from catalog import CatalogService


class CatalogServiceTests(unittest.TestCase):
    def test_uses_supplied_reader(self):
        self.assertEqual(CatalogService({"1": "Supplied title"}).title("1"), "Supplied title")

    def test_strips_id_before_lookup(self):
        reader = Mock()
        reader.get.return_value = "Book"
        self.assertEqual(CatalogService(reader).title(" \t1\n"), "Book")
        reader.get.assert_called_once_with("1")

    def test_rejects_empty_id_before_lookup(self):
        for book_id in ("", " \t\n"):
            with self.subTest(book_id=book_id):
                reader = Mock()
                with self.assertRaises(ValueError):
                    CatalogService(reader).title(book_id)
                reader.get.assert_not_called()

    def test_missing_book_raises_lookup_error(self):
        with self.assertRaises(LookupError):
            CatalogService({}).title("missing")

    def test_empty_title_is_not_missing(self):
        self.assertEqual(CatalogService({"1": ""}).title("1"), "")

    def test_reader_failure_propagates(self):
        failure = RuntimeError("reader unavailable")
        reader = Mock()
        reader.get.side_effect = failure
        with self.assertRaises(RuntimeError) as caught:
            CatalogService(reader).title("1")
        self.assertIs(caught.exception, failure)


if __name__ == "__main__":
    unittest.main()
