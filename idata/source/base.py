import enum


class SourceType(enum.IntEnum):
    Data = 0
    List = 1
    Table = 2
    Tree = 3


class Source:
    def display_name(self):
        return repr(self)

    def type(self):
        raise NotImplementedError


class Proxy:
    pass


class Record:
    """
    like pandas.Series object
    """
    def get(self, name, ctx):
        raise NotImplementedError
