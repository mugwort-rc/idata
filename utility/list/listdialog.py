from PyQt5.QtWidgets import QDialog

from idata.pyqt.models import ListModel

from .ui.listdialog import Ui_ListDialog


class ListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ListDialog()
        self.ui.setupUi(self)

        self.model = ListModel(self)
        self.ui.listView.setModel(self.model)

    def setSeries(self, series):
        self.model.setSeries(series)
