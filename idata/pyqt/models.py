from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtCore import QAbstractItemModel, QAbstractListModel, QAbstractTableModel
from PyQt5.QtCore import QSortFilterProxyModel

import pandas


class SeriesListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.series = pandas.Series()

    def setSeries(self, series):
        self.beginResetModel()
        self.series = series
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.series.index)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Vertical:
            return QVariant()
        return QVariant(str(self.series.index[section]))

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        key = self.series.index[index.row()]
        return QVariant(str(self.series[key]))

    def pandasImpl(self):
        return self.series


class DataFrameTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame = pandas.DataFrame()

    def setDataFrame(self, frame):
        self.beginResetModel()
        self.frame = frame
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.frame.index)

    def columnCount(self, parent=QModelIndex()):
        return len(self.frame.columns)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Vertical:
            return QVariant(str(self.frame.index[section]))
        elif orientation == Qt.Horizontal:
            return QVariant(str(self.frame.columns[section]))
        return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        y = self.frame.index[index.row()]
        x = self.frame.columns[index.column()]
        return QVariant(str(self.frame[x][y]))

    def pandasImpl(self):
        return self.frame

    def seriesFromIndex(self, index):
        y = self.frame.index[index]
        return self.frame.ix[y]

    def seriesFromColumn(self, column):
        x = self.frame.columns[column]
        return self.frame[x]


class TableSourceModel(DataFrameTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.source = None

    def setSource(self, source):
        self.source = source
        self.setDataFrame(source.frame)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if self.data is None:
            return QVariant()
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if self.source.config.columns_size <= section:
                # undefined column
                return section
            return self.source.config.columnByIndex(section).display_name
        return QVariant()


class PandasProxyModel(QSortFilterProxyModel):
    def setSourceModel(self, model):
        impl = model.pandasImpl()
        self._index = pandas.Series(True, index=range(impl.index.size))
        columns = [0] if not hasattr(impl, "columns") else impl.columns
        self._columns = pandas.Series(True, index=range(len(columns)))
        super().setSourceModel(model)

    def setIndexFilter(self, index):
        assert all(self._index.index == index.index)
        self.beginResetModel()
        self._index = index
        self.endResetModel()

    def setColumnsFilter(self, columns):
        assert all(self._columns.index == columns.index)
        self.beginResetModel()
        self._columns = columns
        self.endResetModel()

    def indexFilter(self):
        return self._index

    def columnsFilter(self):
        return self._columns

    def columnCount(self, parent=QModelIndex()):
        vc = self._columns.value_counts()
        return vc[True] if True in vc else 0

    def rowCount(self, parent=QModelIndex()):
        vc= self._index.value_counts()
        return vc[True] if True in vc else 0

    def filterAcceptsColumn(self, source_column, source_parent):
        return self._columns[self._columns.index[source_column]]

    def filterAcceptsRow(self, source_row, source_parent):
        return self._index[self._index.index[source_row]]


class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tree = None

    def setTree(self, tree):
        self.beginResetModel()
        self._tree = tree
        self.endResetModel()

    def tree(self):
        return self._tree

    def columnCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return self._tree.columnCount()
        node = parent.internalPointer()
        return node.columnCount()

    def rowCount(self, parent=QModelIndex()):
        if self._tree is None:
            return 0
        if not parent.isValid():
            return 1  # root case
        node = parent.internalPointer()
        return len(node)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation != Qt.Horizontal:
            return QVariant()
        return section

    def data(self, index, role=Qt.DisplayRole):
        if self._tree is None or not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        node = index.internalPointer()
        assert role == Qt.DisplayRole
        return node.data(index.column())

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            return self.createIndex(row, column, self._tree)
        node = parent.internalPointer()
        return self.createIndex(row, column, node.childs[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        parent = node.parent()
        if parent.parent is None:
            return self.index(0, 0, QModelIndex())
        grandpa = parent.parent()
        return self.createIndex(grandpa.childs.index(parent), 0, parent)
