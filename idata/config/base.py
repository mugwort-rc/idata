import re
from collections import defaultdict

from . import assertion
from . import expression
from . import type
from ..utils.excel import name_to_col
from ..utils.slice import make_slice_list


class ConfigBase:
    def evaluate(self, expr):
        raise NotImplementedError


class TableSourceConfig(ConfigBase):
    def __init__(self, **kwargs):
        self.args = kwargs
        self._init()

    def _init(self):
        self.column_configs = []
        self.column_name2index = {}
        self.column_alias2index = {}
        for i, column_config in enumerate(self.args.get("columns", [])):
            column = TableColumnConfig(self, column_config)
            assert column.name not in self.column_name2index
            self.column_name2index[column.name] = i
            for alias in column.aliases:
                assert alias not in self.column_alias2index
                self.column_alias2index[alias] = i
            self.column_configs.append(column)
        self.startColumn = (self.column_configs[0].n or 0) if self.column_configs else 0

        self.prepare_assertions = defaultdict(list)
        for assert_config in self.args.get("asserts", {}).get("prepare", []):
            a = assertion.RowAssertion(self, assert_config)
            self.prepare_assertions[assert_config["row"]].append(a)

    def evaluate(self, expr):
        if expression.is_config_expr(expr):
            exprs = expr[len("$config@"):].split("@")
            return expression.evaluate_value(self.args, exprs)
        raise NotImplementedError

    def _raw_index_columns(self):
        tmp = []
        current = 0
        for column in self.column_configs:
            if column.n is not None:
                current = column.n
            tmp.append(current)
            current += 1
        return tmp

    def _raw_index_exclude(self, row):
        columns = self._raw_index_columns()
        return [x for x in range(len(row)) if x not in columns]

    def column(self, name):
        return self.columnByIndex(self.column_name2index[name])

    def columnByIndex(self, index):
        return self.column_configs[index]

    def columnType(self, name):
        return self.column(name).type()

    def qualityColumns(self):
        return [x for x in self.column_configs if x.is_qualitative()]

    def quantityColumns(self):
        return [x for x in self.column_configs if x.is_quantitative()]

    def is_simple(self):
        return "simpleTable" in self.args["type"]

    def is_stacked(self):
        return "stackedTable" in self.args["type"]

    @property
    def survey_name(self):
        return self.args.get("survey", {}).get("name")

    @property
    def survey_title(self):
        return self.args.get("title")

    @property
    def startIndex(self):
        return self.args.get("startIndex", 0)

    @property
    def columns(self):
        return [x.name for x in self.column_configs]

    @property
    def stacked(self):
        return StackedConfig(self, self.args.get("stacked", {}))


class TableColumnConfig:
    def __init__(self, config, column_config):
        self.config = config
        self.column_config = column_config

    def __repr__(self):
        title = self.config.survey_title
        if len(title) > 15:
            title = title[:12] + "..."
        return '<Column: {}:{}:"{}">'.format(self.config.survey_name, title, self.display_name)

    def type(self):
        t = self.column_config.get("type")
        if t is None:
            return type.ObjectType()
        elif t == "str":
            return type.StrType()
        elif t == "int":
            return type.IntType()
        elif t == "float":
            return type.FloatType()
        raise NotImplementedError

    def is_qualitative(self):
        return self.column_config["dataType"] == "qualitative"

    def is_quantitative(self):
        return self.column_config["dataType"] == "quantitative"

    @property
    def name(self):
        return self.column_config["name"]

    @property
    def nullable(self):
        return self.column_config.get("nullable", False)

    @property
    def n(self):
        n = self.column_config.get("n")
        if isinstance(n, str):
            n = name_to_col(n)
            self.column_config["n"] = n
        return self.column_config.get("n")

    @property
    def regex(self):
        return self.column_config.get("regex")

    @property
    def aliases(self):
        return self.column_config.get("aliases", [])

    @property
    def display_name(self):
        if self.aliases:
            return self.aliases[0]
        return self.name

    @property
    def unit(self):
        return self.column_config.get("unit")

    @property
    def seeAlso(self):
        for value in self.column_config.get("see", []):
            if expression.is_config_expr(value):
                yield self.config.evaluate(value)
            else:
                yield value


class StackedConfig:
    def __init__(self, config, stacked):
        self.config = config
        self.stacked = stacked

    def __len__(self):
        return len(self.stacked.get("rows", []))

    @property
    def rows(self):
        rows = self.stacked.get("rows", [])
        return [TableRowConfig(self, x) if x else None for x in rows]


class TableRowConfig:
    def __init__(self, config, row_config):
        self.config = config
        self.row_config = row_config

    @property
    def name(self):
        return self.column_config["name"]

    @property
    def aliases(self):
        return self.column_config.get("aliases", [])

    @property
    def display_name(self):
        if self.aliases:
            return self.aliases[0]
        return self.name

    @property
    def unit(self):
        return self.column_config.get("unit")
