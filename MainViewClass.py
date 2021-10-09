import mainwindow
import sounddevice as sd
from threading import Thread
# import asyncio
from PyQt5 import QtWidgets, QtCore
from abc import ABCMeta, abstractmethod


class IMainView():
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def hideLoadBtn(self):
        pass

    @abstractmethod
    def moveTime(self):
        pass

    @abstractmethod
    def stopTimer(self):
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

    @abstractmethod
    def displayTime(self, hh, mm, ss):
        pass

    @abstractmethod
    def showCmb(self):
        pass

    @abstractmethod
    def hideTime(self):
        pass

    @abstractmethod
    def hideCmb(self):
        pass

    @abstractmethod
    def chosenItemCmb(self):
        pass

    @abstractmethod
    def addItemInCmb(self, name):
        pass

    @abstractmethod
    def clearCmb(self):
        pass


class PresenterMainView():

    isPressedPlay = False

    def __init__(self, iMainView: IMainView, model):
        super().__init__()
        self.model = model
        self.iMainView = iMainView
        self.presenterLoadView = None
        self.stopTimer = False
        self.hh, self.mm, self.ss = [0]*3

    def setPresenterLoad(self, presenter):
        self.presenterLoadView = presenter

    def startListen(self):
        thr1 = Thread(target=self.model.startListen, args=())
        thr1.start()
        pass

    def stopTime(self):
        self.iMainView.stopTimer()

    def clearCmb(self):
        self.iMainView.clearCmb()

    def openLyricsView(self):
        self.presenterLoadView.iLoadView.showView()

    def showBtn(self):
        if not self.iMainView.isListenBarVisible():
            self.iMainView.showButtonStartListen()

    def addItemInCmb(self, name):
        self.iMainView.addItemInCmb(name)

    def onStartListenBtnClicked(self):
        self.iMainView.hideButtonStartListen()
        self.iMainView.showListenBar()
        self.iMainView.hideCmb()
        self.model.setDeviceId(self.iMainView.chosenItemCmb())

    def moveTime(self):
        self.iMainView.moveTime()

    def showCmb(self):
        self.iMainView.showCmb()

    def onRecBtnClicked(self):
        if not self.stopTimer:
            self.ss += 1
            if self.ss == 60:
                self.mm += 1
                self.ss = 0
            if self.mm == 60:
                self.hh += 1
                self.mm = 0
            self.iMainView.displayTime(self.hh, self.mm, self.ss)

    def onViewLoaded(self):
        self.iMainView.onViewLoaded()

    def stopTimerTag(self):
        self.stopTimer = True

    def resumeTimerTag(self):
        self.stopTimer = False

    def pauseListen(self):
        self.model.pauseListen()

    def showResBtn(self):
        self.iMainView.showBtnShowResult()

    def hideBarAndShowBtn(self):
        self.iMainView.hideListenBar()
        self.iMainView.hideLoadBtn()

    def hideTime(self):
        self.iMainView.hideTime()

    def timerContinue(self):
        self.stopTimer = False

    def stopListen(self):
        self.model.stopListen()

    def hideListenBar(self):
        self.iMainView.hideListenBar()

    def resumeListen(self):
        self.model.resumeListen()

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
        self.timer = QtCore.QTimer(interval=1000, timeout=self.updateTime)
        self.showResBtn.clicked.connect(self.onShowResClicked)
        self.stopBtn.clicked.connect(self.onStopClicked)
        self.pauseBtn.clicked.connect(self.onPauseClicked)
        self.recBtn.clicked.connect(self.onRecBtnClicked)
        self.playBtn.clicked.connect(self.onPlayBtnClicked)

    def onStopClicked(self):
        self.presenterMainView.showResBtn()
        self.presenterMainView.hideBarAndShowBtn()
        self.presenterMainView.moveTime()
        self.presenterMainView.stopTime()
        self.presenterMainView.stopListen()
        self.presenterMainView.stopTimerTag()

    def resumeTimer(self):
        self.timer.start()

    def onPlayBtnClicked(self):
        self.resumeTimer()
        self.presenterMainView.resumeTimerTag()
        self.presenterMainView.resumeListen()

    def stopTimer(self):
        self.timer.stop()

    def hideRecBtn(self):
        self.recBtn.hide()

    def moveTime(self):
        self.tEdit.setGeometry(430, 410, 131, 31)

    def onPauseClicked(self):
        self.presenterMainView.stopTimerTag()
        self.presenterMainView.pauseListen()

    def moveLoadBtn(self):
        self.loadBtn.setGeometry(340, 70,271, 51)

    def onRecBtnClicked(self):
        self.timer.start()
        self.hideRecBtn()
        self.presenterMainView.timerContinue()
        self.presenterMainView.onRecBtnClicked()
        self.presenterMainView.startListen()

    def updateTime(self):
        self.presenterMainView.onRecBtnClicked()

    def hideLoadBtn(self):
        self.loadBtn.hide()

    def clearCmb(self):
        self.cmb.clear()

    def displayTime(self, hh, mm, ss):
        self.tEdit.setTime(QtCore.QTime(hh, mm, ss))

    def setPres(self, pres):
        self.presenterMainView.setPresenterLoad(pres)

    def onViewLoaded(self):
        self.setWindowTitle('Проверить стих')
        self.hideButtonStartListen()
        self.hideBtnShowResult()
        self.hideCmb()
        self.hideListenBar()
        self.hideTime()
        self.configCmb()

    def configCmb(self):
        self.cmb.setEditable(False)

    def hideCmb(self):
        self.cmb.hide()

    def showCmb(self):
        self.cmb.show()

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

    def hideTime(self):
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
        self.moveLoadBtn()
        self.presenterMainView.onStartListenBtnClicked()
        pass

    def chosenItemCmb(self):
        return self.cmb.currentIndex()

    def addItemInCmb(self, name):
        self.cmb.addItem(name)

    def givePresenter(self):
        return self.presenterMainView

    def onShowResClicked(self):
        pass