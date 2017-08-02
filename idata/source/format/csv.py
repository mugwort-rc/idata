import csv

from ...config.base import TableSourceConfig
from .. import table
from ...utils import digests


class CommaSeparatedValue(table.TableSource):
    def __init__(self, identifier, frame):
        # TODO: filepath etc... into config?
        super().__init__(TableSourceConfig(), frame)
        self.identifier = identifier

    def abstract(self):
        # TODO:
        return ""

    def identifier(self):
        return self.identifier

    def index(self):
        return self.frame.index.tolist()

    def columns(self):
        return self.frame.columns.tolist()

    @staticmethod
    def load(filepath, **kwargs):
        return self.load_by_python(filepath, **kwargs)

    @staticmethod
    def load_by_python(filepath, **kwargs):
        sha1 = digests.sha1(filepath)
        identifier = "sha1:" + sha1
        table = []
        encoding = kwargs.get("encoding", "utf-8")
        with open(filepath, "r", encoding=encoding) as fp:
            table = list(csv.reader(fp))
        return CommaSeparatedValue(identifier, table)

    @staticmethod
    def load_by_pandas(filepath, **kwargs):
        sha1 = digests.sha1(filepath)
        identifier = "sha1:" + sha1
        import pandas
        frame = pandas.load_csv(filepath, **kwargs)
        return CommaSeparatedValue(identifier, frame)
