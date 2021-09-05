import loadLyrics
from PyQt5 import QtWidgets
from abc import ABCMeta, abstractmethod


class ILoadView():
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def showView(self):
        pass

    @abstractmethod
    def hideView(self):
        pass

    @abstractmethod
    def setTitle(self, title):
        pass

    @abstractmethod
    def setModelTxt(self, txt):
        pass

    @abstractmethod
    def openFile(self):
        pass


class PresenterLoadView():
    def __init__(self, iLoadView: ILoadView, model):
        super().__init__()
        self.model = model
        self.iLoadView = iLoadView
        self.presenterTextCatcher = None
        self.presenterMainV = None

    def setPresenterTextCatcher(self, pres):
        self.presenterTextCatcher = pres

    def setpresenterMainV(self, pres):
        self.presenterMainV = pres

    def openTextCatcher(self):
        self.presenterTextCatcher.iTextCatcher.showView()

    def onTextLoadClicked(self):
        self.iLoadView.openFile()

    def onTextLoaded(self, filename):
        text = ''
        if filename != '':
            with open(filename, 'r') as f:
                text = f.read()
            text = text.replace('\n', ' ')
            self.model.setTextLyr(text)
            self.hideView()
            self.presenterMainV.showBtn()
        pass

    def onViewLoaded(self):
        self.iLoadView.setTitle("Загрузить стих")
        self.hideView()

    def hideView(self):
        self.iLoadView.hideView()

    def showBtn(self):
        self.presenterMainV.showBtn()


class LoadView(QtWidgets.QDialog, loadLyrics.Ui_Dialog, ILoadView):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setupUi(self)
        self.presenterLoadView = PresenterLoadView(self, self.model)
        self.loadFileBtn.clicked.connect(self.onLoadFileClicked)
        self.loadTextBtn.clicked.connect(self.onLoadTextClicked)
        self.presenterLoadView.onViewLoaded()

    def setModelTxt(self, txt):
        self.model.setTextLyr(txt)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def onLoadTextClicked(self):
        self.presenterLoadView.onTextLoadClicked()

    def openFile(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Text Files(*.txt)")
        self.presenterLoadView.onTextLoaded(filename)

    def hideView(self):
        self.hide()

    def setPresenterLoadV(self, pres):
        self.presenterLoadView.setPresenterTextCatcher(pres)

    def onLoadFileClicked(self):
        self.presenterLoadView.openTextCatcher()
        pass

    def setPresenterMainV(self, pres):
        self.presenterLoadView.setpresenterMainV(pres)
        pass

    def givePresenter(self):
        return self.presenterLoadView

    def showView(self):
        self.show()