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
