import mainwindow
from PyQt5 import QtWidgets
from abc import ABCMeta, abstractmethod

class IMainView():
    _metaclass_ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def hideLoadBtn(self):
        pass

    @abstractmethod
    def showButtonStartListen(self):
        pass

    @abstractmethod
    def isListenBarVisible(self):
        pass

    @abstractmethod
    def showListenBar(self):
        pass

    @abstractmethod
    def hideListenBar(self):
        pass

    @abstractmethod
    def setPres(self, pres):
        pass

    @abstractmethod
    def hideButtonStartListen(self):
        pass

    @abstractmethod
    def showBtnShowResult(self):
        pass

    @abstractmethod
    def hideBtnShowResult(self):
        pass

    @abstractmethod
    def onViewLoaded(self):
        pass


class PresenterMainView():
    def __init__(self, iMainView: IMainView, model):
        super().__init__()
        self.model = model
        self.iMainView = iMainView
        self.presenterLoadView = None

    def setPresenterLoad(self, presenter):
        self.presenterLoadView = presenter

    def openLyricsView(self):
        self.presenterLoadView.iLoadView.showView()

    def showBtn(self):
        if not self.iMainView.isListenBarVisible():
            self.iMainView.showButtonStartListen()

    def onStartListenBtnClicked(self):
        self.iMainView.hideButtonStartListen()
        self.iMainView.showListenBar()

    def onViewLoaded(self):
        self.iMainView.onViewLoaded()

    def showResBtn(self):
        self.iMainView.showBtnShowResult()

    def hideBarAndShowBtn(self):
        self.iMainView.hideListenBar()
        self.iMainView.hideLoadBtn()

    def hideListenBar(self):
        self.iMainView.hideListenBar()

class MainView(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow, IMainView):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.presenterMainView = PresenterMainView(self, self.model)
        self.setupUi(self)
        self.show()
        self.presenterMainView.onViewLoaded()
        self.loadBtn.clicked.connect(self.onLoadBtnClicked)
        self.startListenBtn.clicked.connect(self.onStartListenBtnClicked)
        self.showResBtn.clicked.connect(self.onShowResClicked)
        self.stopBtn.clicked.connect(self.onStopClicked)

    def onStopClicked(self):
        self.presenterMainView.showResBtn()
        self.presenterMainView.hideBarAndShowBtn()

    def hideLoadBtn(self):
        self.loadBtn.hide()

    def setPres(self, pres):
        self.presenterMainView.setPresenterLoad(pres)

    def onViewLoaded(self):
        self.setWindowTitle('Проверить стих')
        self.hideButtonStartListen()
        self.hideBtnShowResult()
        self.hideListenBar()

    def isListenBarVisible(self):
        return self.recBtn.isVisible()

    def showButtonStartListen(self):
        self.startListenBtn.show()

    def hideButtonStartListen(self):
        self.startListenBtn.hide()

    def hideListenBar(self):
        self.recBtn.hide()
        self.pauseBtn.hide()
        self.playBtn.hide()
        self.stopBtn.hide()
        self.tEdit.hide()

    def showListenBar(self):
        self.recBtn.show()
        self.pauseBtn.show()
        self.playBtn.show()
        self.stopBtn.show()
        self.tEdit.show()

    def onLoadBtnClicked(self):
        self.presenterMainView.openLyricsView()
        pass

    def showBtnShowResult(self):
        self.showResBtn.show()

    def hideBtnShowResult(self):
        self.showResBtn.hide()

    def onStartListenBtnClicked(self):
        self.presenterMainView.onStartListenBtnClicked()
        pass

    def givePresenter(self):
        return self.presenterMainView

    def onShowResClicked(self):
        pass