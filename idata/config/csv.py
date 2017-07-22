import csv

from .base import TableSourceConfig
from ..source.table import TableSource, StackedTableSource


class CSVTableSourceConfig(TableSourceConfig):
    def load(self, path, encoding="utf-8"):
        if hasattr(path, "read"):
            return self._load(path)
        with open(path, "r", encoding=encoding) as fp:
            return self._load(fp)

    def _load(self, fp):
        reader = csv.reader(fp)
        for i, row in enumerate(reader):
            if i in self.prepare_assertions:
                for v in self.prepare_assertions[i]:
                    if not v.check(row):
                        msg = v.error_message(row)
                        raise AssertionError("row: {}: {}".format(i, msg))
            if i + 1 == self.startIndex:
                break
        exclude = self._raw_index_exclude(row)
        # TODO: StackedTableSource
        import pandas
        df = pandas.DataFrame.from_records(reader, exclude=exclude)
        if exclude == [0]:
            df = df.drop(0, axis=1)
        df.columns = self.columns
        if self.is_simple():
            return TableSource(self, df)
        elif self.is_stacked():
            return StackedTableSource(self, df)
        raise NotImplementedError

    def _raw_index_exclude(self, row):
        columns = self._raw_index_columns()
        return [x for x in range(len(row)) if x not in columns]
