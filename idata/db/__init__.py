import builtins
import os

from .. import config
from ..utils import digests


class Database:
    def __init__(self, path, configurations):
        self.path = path
        self.configurations = configurations
        self.digests = {}
        self._init()

    def _init(self):
        for path, conf in self.configurations.items():
            for digest in conf.digests():
                self.digests[digest] = conf

    def detect_by_file(self, path):
        def _detect_by_file(fp):
            impl = digests.DigestCalculator.sha1()
            impl.calc(fp)
            digest = "sha1:{}".format(impl.hexdigest())
            if digest not in self.digests:
                return None
            return self.digests[digest]
        if hasattr(path, "read"):
            return _detect_by_file(path)
        with builtins.open(path, "rb") as fp:
            return _detect_by_file(fp)

    def search(self, words):
        if isinstance(words, str):
            words = [words]
        columns = []
        def _search(text):
            return all(map(lambda x: x in text, words))
        for path, conf in self.configurations.items():
            for key in conf.columns:
                column = conf.column(key)
                if _search(column.name):
                    columns.append(column)
                    continue
                for alias in column.aliases:
                    if _search(alias):
                        columns.append(column)
                        break
        return columns

    @staticmethod
    def open(path):
        configurations = {}
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                root, ext = os.path.splitext(filename)
                if ext != ".yml":
                    continue
                path = os.path.join(dirpath, filename)
                configurations[path] = config.load_yaml(path)
        return Database(path, configurations)


open = Database.open
