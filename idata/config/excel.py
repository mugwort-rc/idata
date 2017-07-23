import xlrd

from .base import TableSourceConfig
from ..source.table import TableSource, StackedTableSource


class ExcelTableSourceConfig(TableSourceConfig):
    def load(self, path):
        assert isinstance(path, str)
        return self._load(path)

    def _load(self, path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_name(self.args["sheetName"])
        for i in range(sheet.nrows):
            row = list(map(lambda x: x.value, sheet.row(i)))
            if i in self.prepare_assertions:
                for v in self.prepare_assertions[i]:
                    if not v.check(row):
                        msg = v.error_message(row)
                        raise AssertionError("row: {}: {}".format(i, msg))
            if i + 1 == self.startIndex:
                break
        exclude = self._raw_index_exclude(row)
        def gen_table():
            for i in range(self.startIndex, sheet.nrows):
                yield list(map(lambda x: x.value, sheet.row(i)))
        # TODO: StackedTableSource
        import pandas
        df = pandas.DataFrame.from_records(gen_table(), exclude=exclude)
        if exclude == [0]:
            df = df.drop(0, axis=1)
        df.columns = self.columns
        if self.is_simple():
            return TableSource(self, df)
        elif self.is_stacked():
            return StackedTableSource(self, df)
        raise NotImplementedError
