import os

from .. import config


class Database:
    def __init__(self, path, configurations):
        self.path = path
        self.configurations = configurations

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
