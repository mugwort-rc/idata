import hashlib
import shutil


class DigestCalculator:
    def __init__(self, impl):
        self.impl = impl

    def calc(self, fp):
        shutil.copyfileobj(fp, self)

    def write(self, data):
        self.impl.update(data)

    def hexdigest(self):
        return self.impl.hexdigest()

    @staticmethod
    def sha1():
        return DigestCalculator(hashlib.sha1())


def sha1(fileobj):
    if not hasattr(fileobj, "read"):
        with open(fileobj, "rb") as fp:
            return sha1(fp)
    dc = DigestCalculator.sha1()
    dc.calc(fileobj)
    return dc.hexdigest()
