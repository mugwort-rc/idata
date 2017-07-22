# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'utility/list/ui/listdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ListDialog(object):
    def setupUi(self, ListDialog):
        ListDialog.setObjectName("ListDialog")
        ListDialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(ListDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.listView = QtWidgets.QListView(ListDialog)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)

        self.retranslateUi(ListDialog)
        QtCore.QMetaObject.connectSlotsByName(ListDialog)

    def retranslateUi(self, ListDialog):
        _translate = QtCore.QCoreApplication.translate
        ListDialog.setWindowTitle(_translate("ListDialog", "ListView"))

