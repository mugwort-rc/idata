from unittest import TestCase

from .. import csv
from .. import variable


class TestVariableExpr(TestCase):
    def setUp(self):
        self.config = csv.CSVTableSourceConfig(columns=[{
            "name": "a",
            "type": "str",
        }])

    def test_evaluate(self):
        ctx = variable.VariableContext(self.config)
        expr = variable.VariableExpr(ctx, "${a}")
        record = dict(a="hoge")
        self.assertEqual(expr.evaluate(record), repr("hoge"))


class TestVariableContext(TestCase):
    def setUp(self):
        self.config = csv.CSVTableSourceConfig(columns=[{
            "name": "a",
            "type": "str",
        }])

    def test_evaluate(self):
        ctx = variable.VariableContext(self.config)
        record = dict(a="hoge")
        self.assertEqual(ctx.evaluate("a", record), "hoge")
        self.assertEqual(ctx.evaluate("a", record, raw=False), repr("hoge"))
