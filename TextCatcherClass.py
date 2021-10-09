import enterLyrics
from PyQt5 import QtWidgets
from abc import ABCMeta, abstractmethod

class ITextCatcher():
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def showView(self):
        pass

    @abstractmethod
    def getWrittenText(self):
        pass

    @abstractmethod
    def givePresenter(self):
        pass

    @abstractmethod
    def hideView(self):
        pass

    @abstractmethod
    def handleErrorInput(self):
        pass


class PresenterTextCatcher():
    def __init__(self, iTextCatcher, model):
        super().__init__()
        self.iTextCatcher = iTextCatcher
        self.model = model
        self.presenterLoadView = None

    def setPresLoadV(self, pres):
        self.presenterLoadView = pres

    def onReadyBtnClicked(self):
        txt = self.iTextCatcher.getWrittenText()
        if txt != '':
            self.model.setTextLyr(txt.replace('\n', ' '))
            self.iTextCatcher.hideView()
            self.presenterLoadView.hideView()
            self.presenterLoadView.showBtn()
            self.presenterLoadView.showCmbMain()
        else:
            self.iTextCatcher.handleErrorInput()
        pass


class TextCatcher(QtWidgets.QDialog, enterLyrics.Ui_Dialog, ITextCatcher):
    def __init__(self, model):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Введите текст')
        self.model = model
        self.presenterTextCatcher = PresenterTextCatcher(self, model)
        self.hide()
        self.readyBtn.clicked.connect(self.onReadyBtnClicked)

    def showView(self):
        self.show()

    def hideView(self):
        self.hide()

    def givePresenter(self):
        return self.presenterTextCatcher

    def setPresenterLoadV(self, pres):
        self.presenterTextCatcher.setPresLoadV(pres)

    def getWrittenText(self):
        return self.tEdit.toPlainText()

    def onReadyBtnClicked(self):
        self.presenterTextCatcher.onReadyBtnClicked()

    def handleErrorInput(self):
        QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введите текст', QtWidgets.QMessageBox.Ok)