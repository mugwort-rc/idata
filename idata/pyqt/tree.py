import weakref


class TreeBase:
    def __init__(self, parent=None):
        self.parent = None if parent is None else weakref.ref(parent)

    def __len__(self):
        return len(self.childs)

    def columnCount(self):
        raise NotImplementedError

    def data(self, key):
        raise NotImplementedError

    def has_childs(self):
        return len(self) > 0

    @property
    def childs(self):
        raise NotImplementedError


from lxml import etree


class DOMTree(TreeBase):
    def __init__(self, elem, parent=None):
        super().__init__(parent)
        self.elem = elem
        self._childs = None

    def columnCount(self):
        return 2

    def data(self, key):
        if key == 0:
            return "Element"
        else:
            return self.elem.tag

    @property
    def childs(self):
        if self._childs is not None:
            return self._childs
        self._childs = [DOMTree(x, self) for x in self.elem]
        if self.elem.text and self.elem.text.strip():
            self._childs.insert(0, TextNode(self.elem.text, self))
        if self.elem.tail and self.elem.tail.strip():
            self._childs.append(TailNode(self.elem.tail, self))
        return self._childs

    @staticmethod
    def fromstring(xml):
        return DOMTree(etree.fromstring(xml))


class TextNode(TreeBase):

    NAME = "text()"

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self._childs = None

    def columnCount(self):
        return 2

    def data(self, key):
        if key == 0:
            return "text()"
        else:
            return self.text

    @property
    def childs(self):
        return []


class TailNode(TextNode):
    NAME = "tail()"
