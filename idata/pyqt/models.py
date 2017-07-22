from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel

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
            return self.source.config.columnByIndex(section).display_name
        return QVariant()
