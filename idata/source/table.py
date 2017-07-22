import pandas

from .base import Source
from .base import Record


class TableSource(Source):
    def __init__(self, config, data, columns=None, index=None):
        self.config = config
        self.frame = pandas.DataFrame(data, columns=columns, index=index)

    def record(self, index):
        series = self.frame[index]
        # TODO: TableRecord.sourceExpr()
        return TableRecord(series, None, None)


class TableRecord(Record):
    def __init__(self, series, index_ctx, columns_ctx):
        self.series = series
        self.index_ctx = index_ctx
        self.columns_ctx = columns_ctx

    def __getitem__(self, key):
        return self.series[key]

    def get(self, name, default=None):
        return self.series.get(name, default=default)

    def sourceExpr(self, name):
        index_expr = self.index_ctx.sourceExpr()
        column_expr = self.columns_ctx.sourceExpr(name)
        return index_expr + column_expr
