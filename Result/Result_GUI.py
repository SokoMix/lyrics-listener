from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(939, 832)
        font = QtGui.QFont()
        font.setPointSize(15)
        Dialog.setFont(font)
        self.resTxt = QtWidgets.QTextEdit(Dialog)
        self.resTxt.setGeometry(QtCore.QRect(10, 59, 921, 701))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.resTxt.setFont(font)
        self.resTxt.setObjectName("resTxt")
        self.resTxt.setReadOnly(True)
        self.lbl = QtWidgets.QLabel(Dialog)
        self.lbl.setGeometry(QtCore.QRect(0, 0, 941, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.lbl.setFont(font)
        self.lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl.setAutoFillBackground(False)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.readyBtn = QtWidgets.QPushButton(Dialog)
        self.readyBtn.setGeometry(QtCore.QRect(343, 770, 271, 51))
        self.readyBtn.setObjectName("readyBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl.setText(_translate("Dialog", "Результаты проверки:"))
        self.readyBtn.setText(_translate("Dialog", "Готово"))
