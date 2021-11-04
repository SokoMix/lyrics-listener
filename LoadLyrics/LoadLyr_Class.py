from LoadLyrics import LoadLyrics_GUI
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

    @abstractmethod
    def unlock(self):
        pass


class PresenterLoadView():
    def __init__(self, iLoadView: ILoadView, model):
        super().__init__()
        self.model = model
        self.iLoadView = iLoadView
        self.presenterTextCatcher = None
        self.presenterMainV = None
        self.isOpenCmb = False

    def setPresenterTextCatcher(self, pres):
        self.presenterTextCatcher = pres

    def setpresenterMainV(self, pres):
        self.presenterMainV = pres

    def openTextCatcher(self):
        self.presenterTextCatcher.iTextCatcher.showView()

    def onTextLoadClicked(self):
        self.iLoadView.openFile()

    def unlockWithMain(self):
        self.iLoadView.unlock()
        self.presenterMainV.unlock()

    def unlock(self):
        self.iLoadView.unlock()

    def onTextLoaded(self, filename):
        text = ''
        if filename != '':
            with open(filename, 'r') as f:
                text = f.read()
            text = text.replace('\n', ' ')
            self.model.setTextLyr(text)
            self.hideView()
            if not self.isOpenCmb:
                self.presenterMainV.showBtn()
                self.showCmbMain()
                self.isOpenCmb = True

    def showCmbMain(self):
        self.presenterMainV.configCmb()

    def onViewLoaded(self):
        self.iLoadView.setTitle('Ввод текста')
        self.hideView()

    def hideView(self):
        self.iLoadView.hideView()

    def showBtn(self):
        self.presenterMainV.showBtn()

    def unlockMainView(self):
        self.presenterMainV.unlock()


class LoadView(QtWidgets.QDialog, LoadLyrics_GUI.Ui_Dialog, ILoadView):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setupUi(self)
        self.presenterLoadView = PresenterLoadView(self, self.model)
        self.loadFileBtn.clicked.connect(self.onLoadTextClicked)
        self.loadTextBtn.clicked.connect(self.onLoadFileClicked)
        self.presenterLoadView.onViewLoaded()

    def closeEvent(self, QCloseEvent):
        self.presenterLoadView.unlockMainView()

    def unlock(self):
        self.setDisabled(False)

    def setModelTxt(self, txt):
        self.model.setTextLyr(txt)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def onLoadFileClicked(self):
        self.presenterLoadView.onTextLoadClicked()

    def openFile(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Text Files(*.txt)")
        self.presenterLoadView.onTextLoaded(filename)

    def hideView(self):
        self.hide()

    def setPresenterLoadV(self, pres):
        self.presenterLoadView.setPresenterTextCatcher(pres)

    def onLoadTextClicked(self):
        self.setDisabled(True)
        self.presenterLoadView.openTextCatcher()
        pass

    def setPresenterMainV(self, pres):
        self.presenterLoadView.setpresenterMainV(pres)
        pass

    def givePresenter(self):
        return self.presenterLoadView

    def showView(self):
        self.show()
