from .base import Source, SourceType
from .base import Proxy
from .base import Record


class TableSource(Source):
    def __init__(self, config, data, columns=None, index=None):
        self.config = config
        import pandas
        self.frame = pandas.DataFrame(data, columns=columns, index=index)

    def type(self):
        return SourceType.Table

    def record(self, index):
        series = self.frame[index]
        # TODO: TableRecord.sourceExpr()
        return TableRecord(series, None, None)


class StackedTableSource(TableSource):
    def stackedCount(self):
        rows = self.config.stacked.rows
        rowCount = len(rows)
        assert len(self.frame.index) % rowCount == 0
        return len(self.frame.index) // rowCount

    def stacked(self, index):
        assert index < self.stackedCount()
        rows = self.config.stacked.rows
        rowCount = len(rows)
        filter = [i + (rowCount * index) for i,x in enumerate(rows) if x]
        return StackedTable(self, index, self.frame[self.frame.index.isin(filter)])


class StackedTable(Proxy):
    def __init__(self, source, index, frame):
        self.source = source
        self.index = index
        self.frame = frame

    def record(self, index):
        series = self.frame[frame.index[index]]
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
