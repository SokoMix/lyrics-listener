from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(637, 181)
        font = QtGui.QFont()
        font.setPointSize(15)
        Dialog.setFont(font)
        self.lbl = QtWidgets.QLabel(Dialog)
        self.lbl.setGeometry(QtCore.QRect(150, 10, 371, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lbl.setFont(font)
        self.lbl.setObjectName("lbl")
        self.loadTextBtn = QtWidgets.QPushButton(Dialog)
        self.loadTextBtn.setGeometry(QtCore.QRect(30, 95, 231, 51))
        self.loadTextBtn.setObjectName("loadFileBtn")
        self.loadFileBtn = QtWidgets.QPushButton(Dialog)
        self.loadFileBtn.setGeometry(QtCore.QRect(373, 95, 231, 51))
        self.loadFileBtn.setObjectName("loadTextBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl.setText(_translate("Dialog", "Выберите способ загрузки стиха"))
        self.loadTextBtn.setText(_translate("Dialog", "Загрузить файл"))
        self.loadFileBtn.setText(_translate("Dialog", "Написать текст"))
