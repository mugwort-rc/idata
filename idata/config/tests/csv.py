from unittest import TestCase

from .. import csv

class TestCSVTableSourceConfig(TestCase):
    def test_evaluate_dict(self):
        kwargs = {
            "constants": {
                "e": 2.71828,
            },
        }
        c = csv.CSVTableSourceConfig(**kwargs)
        self.assertEqual(c.evaluate("$config@constants@e"), 2.71828)

    def test_evaluate_list(self):
        kwargs = {
            "constants": {
                "list": [{
                    "n": 1,
                    "sqrt": 1.0,
                }, {
                    "n": 2,
                    "sqrt": 1.41421,
                }, {
                    "n": 3,
                    "sqrt": 1.73205,
                },],
            },
        }
        c = csv.CSVTableSourceConfig(**kwargs)
        self.assertEqual(c.evaluate("$config@constants@list[2]@sqrt"), 1.73205)
