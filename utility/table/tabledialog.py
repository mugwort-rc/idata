from PyQt5.QtWidgets import QDialog

from idata.pyqt.models import TableSourceModel

from .ui.tabledialog import Ui_TableDialog


class TableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TableDialog()
        self.ui.setupUi(self)

        self.model = TableSourceModel(self)
        self.ui.tableView.setModel(self.model)

    def setSource(self, source):
        self.model.setSource(source)
