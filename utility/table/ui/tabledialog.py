# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'utility/table/ui/tabledialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TableDialog(object):
    def setupUi(self, TableDialog):
        TableDialog.setObjectName("TableDialog")
        TableDialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(TableDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(TableDialog)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)

        self.retranslateUi(TableDialog)
        QtCore.QMetaObject.connectSlotsByName(TableDialog)

    def retranslateUi(self, TableDialog):
        _translate = QtCore.QCoreApplication.translate
        TableDialog.setWindowTitle(_translate("TableDialog", "TableView"))

