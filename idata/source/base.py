

class Source:
    pass


class Proxy:
    pass


class Record:
    """
    like pandas.Series object
    """
    def get(self, name, ctx):
        raise NotImplementedError
