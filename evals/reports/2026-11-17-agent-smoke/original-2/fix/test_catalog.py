import unittest
from unittest.mock import Mock

from catalog import CatalogService


class CatalogServiceTests(unittest.TestCase):
    def test_supplied_reader_and_trimmed_id(self):
        reader = Mock()
        reader.get.return_value = "Injected title"
        self.assertEqual(CatalogService(reader).title(" \t1\n"), "Injected title")
        reader.get.assert_called_once_with("1")

    def test_empty_id_rejected_before_lookup(self):
        for book_id in ("", " \t\n"):
            with self.subTest(book_id=book_id):
                reader = Mock()
                with self.assertRaises(ValueError):
                    CatalogService(reader).title(book_id)
                reader.get.assert_not_called()

    def test_missing_book(self):
        with self.assertRaises(LookupError):
            CatalogService({}).title("missing")

    def test_reader_failure_propagates(self):
        failure = RuntimeError("Reader unavailable")
        reader = Mock()
        reader.get.side_effect = failure
        with self.assertRaises(RuntimeError) as raised:
            CatalogService(reader).title("1")
        self.assertIs(raised.exception, failure)
        reader.get.assert_called_once_with("1")

    def test_empty_title_is_not_missing(self):
        self.assertEqual(CatalogService({"1": ""}).title("1"), "")


if __name__ == "__main__":
    unittest.main()
