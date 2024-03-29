from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(689, 630)
        font = QtGui.QFont()
        font.setPointSize(15)
        Dialog.setFont(font)
        self.lbl = QtWidgets.QLabel(Dialog)
        self.lbl.setGeometry(QtCore.QRect(270, -7, 181, 41))
        self.lbl.setObjectName("lbl")
        self.tEdit = QtWidgets.QTextEdit(Dialog)
        self.tEdit.setGeometry(QtCore.QRect(3, 29, 681, 541))
        self.tEdit.setTabletTracking(False)
        self.tEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tEdit.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tEdit.setObjectName("tEdit")
        self.readyBtn = QtWidgets.QPushButton(Dialog)
        self.readyBtn.setGeometry(QtCore.QRect(230, 575, 231, 51))
        self.readyBtn.setObjectName("readyBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl.setText(_translate("Dialog", "Введите текст"))
        self.readyBtn.setText(_translate("Dialog", "Готово"))
