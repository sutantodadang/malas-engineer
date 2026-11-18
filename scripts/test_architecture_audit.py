#!/usr/bin/env python3
"""Tests both known-bad and known-good files. Scanner findings are not proof."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from architecture_audit import python_scan, other_scan, scan

ROOT=Path(__file__).resolve().parents[1]
class ArchitectureAuditTests(unittest.TestCase):
    def test_checkout_parent_does_not_set_file_role(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'services' / 'checkout'
            root.mkdir(parents=True)
            (root / 'bootstrap.py').write_text('repo = BookRepository()\n', encoding='utf-8')
            (root / 'book_service.py').write_text('repo = BookRepository()\n', encoding='utf-8')
            self.assertEqual([Path(row['file']).name for row in scan(root)], ['book_service.py'])

    def test_dependency_directories_are_never_entered(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ignored = root / 'node_modules'
            ignored.mkdir()
            visited = []
            scandir = os.scandir

            def record(path):
                visited.append(Path(path))
                return scandir(path)

            with patch('os.scandir', record):
                scan(root)
            self.assertNotIn(ignored, visited)

    def test_missing_scan_root_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                scan(Path(tmp) / 'missing')

    def test_python_test_module_is_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test_order_service.py'
            path.write_text('repo = OrderRepository()\n', encoding='utf-8')
            self.assertEqual(scan(Path(tmp)), [])

    def test_comment_removal_preserves_source_line_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'order_service.ts'
            path.write_text('/* header\ncontinued\n*/\nnew OrderRepository();\n', encoding='utf-8')
            self.assertEqual(other_scan(path)[0]['line'], 4)

    def test_service_constructs_adapter_and_ignores_injection(self):
        findings = python_scan(ROOT/'evals/fixtures/bad/order_service.py')
        self.assertEqual({x['rule'] for x in findings}, {'SERVICE_CREATES_ADAPTER', 'INJECTED_BUT_UNUSED'})
    def test_handler_direct_db_operation(self):
        self.assertIn('HANDLER_PERSISTENCE_IO', {x['rule'] for x in python_scan(ROOT/'evals/fixtures/bad/order_handler.py')})
    def test_go_new_repo_bad(self):
        self.assertIn('SERVICE_CREATES_ADAPTER', {x['rule'] for x in other_scan(ROOT/'evals/fixtures/bad/payment_service.go')})
    def test_typescript_new_repo_bad(self):
        self.assertIn('SERVICE_CREATES_ADAPTER', {x['rule'] for x in other_scan(ROOT/'evals/fixtures/bad/book_service.ts')})
    def test_good_service_not_flagged(self):
        self.assertEqual(python_scan(ROOT/'evals/fixtures/good/order_service.py'), [])
    def test_real_python_contract_example_not_flagged(self):
        self.assertEqual(scan(ROOT/'examples/python-contract'), [])
    def test_real_go_contract_example_not_flagged(self):
        self.assertEqual(scan(ROOT/'examples/go-contract'), [])
    def test_real_typescript_contract_example_not_flagged(self):
        self.assertEqual(scan(ROOT/'examples/typescript-contract'), [])

if __name__ == '__main__': unittest.main()
