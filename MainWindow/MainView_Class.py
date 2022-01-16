from MainWindow import MVtest
from PyQt5 import QtWidgets, QtCore, QtGui
from abc import ABCMeta, abstractmethod
from pydub import AudioSegment
from threading import Thread
from PyQt5.QtCore import pyqtSignal
import sounddevice as sd
import os


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
    def hideReadyLbl(self):
        pass

    @abstractmethod
    def showReadyLbl(self):
        pass

    @abstractmethod
    def hideHandleLbl(self):
        pass

    @abstractmethod
    def showHandleLbl(self):
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

    @abstractmethod
    def showRes(self, output):
        pass

    @abstractmethod
    def unlock(self):
        pass

    @abstractmethod
    def getLang(self):
        pass

    @abstractmethod
    def showChoiceBtns(self):
        pass

    @abstractmethod
    def hideChoiceBtns(self):
        pass

    @abstractmethod
    def showLoadFileBtn(self):
        pass

    @abstractmethod
    def catalogExecute(self):
        pass

    @abstractmethod
    def hideTable(self):
        pass

    @abstractmethod
    def showTable(self):
        pass

    @abstractmethod
    def showFileResBtn(self):
        pass

    @abstractmethod
    def disableLoadBtns(self):
        pass

    @abstractmethod
    def enableLoadBtns(self):
        pass

class PresenterMainView():

    isPressedPlay = False
    res_sig = None

    def __init__(self, iMainView: IMainView, model, sig):
        super().__init__()
        self.model = model
        self.res_sig = sig
        self.iMainView = iMainView
        self.presenterLoadView = None
        self.resultPres = None
        self.stopTimer = False
        self.hh, self.mm, self.ss = [0]*3
        self.catalogAudio = None

    def hideTable(self):
        self.iMainView.hideTable()

    def setResultPres(self, resv):
        self.resultPres = resv

    def finishHandle(self):
        self.iMainView.hideHandleLbl()
        self.iMainView.showReadyLbl()

    def showTable(self):
        self.iMainView.showTable()

    def setCatalogAudio(self, path):
        self.catalogAudio = path

    def onShowResClicked(self):
        self.model.checkResult()
        self.iMainView.showRes(self.model.getSimilarity())

    def setPresenterLoad(self, presenter):
        self.presenterLoadView = presenter

    def startListen(self):
        self.model.startListen()

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

    def configCmb(self):
        self.iMainView.showCmb()
        self.iMainView.clearCmb()
        self.iMainView.addItemInCmb('Выберите аудиоустройство для записи')
        devices = sd.query_devices()
        input_devices = []
        id = 0
        for items in devices:
            if items['max_input_channels'] > 0:
                input_devices.append(id)
                self.iMainView.addItemInCmb(items['name'])
            id += 1
        self.model.setInputDevices(input_devices)

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

    def saveLang(self):
        lang = self.iMainView.getLang()
        self.model.setLang(lang)
        self.iMainView.hideTable()

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

    def unlock(self):
        self.iMainView.unlock()

    def onLiveListenBtnClicked(self):
        self.iMainView.showCmb()
        self.iMainView.showButtonStartListen()
        self.iMainView.hideChoiceBtns()
        self.configCmb()

    def onFileListenBtnClicked(self):
        self.iMainView.showLoadFileBtn()

    def showChoiceBtns(self):
        self.iMainView.showChoiceBtns()

    def onLoadFileBtnClicked(self):
        dir = self.iMainView.catalogExecute()
        if dir != '':
            self.setCatalogAudio(dir)
            files = os.listdir(self.catalogAudio)
            for i in range(len(files)):
                files[i] = self.catalogAudio+'/'+files[i]
            for i in range(len(files)):
                if files[i][-3:]!='wav':
                    sound = AudioSegment.from_file(files[i])
                    files[i] = files[i][:-3]+'wav'
                    sound.export(files[i], format="wav")
            self.model.setAudioFiles(files)
            self.iMainView.showFileResBtn()

    def sig_showFiles(self):
        self.resultPres.showFiles()
        self.iMainView.enableLoadBtns()

    def checkFilesRes(self):
        self.iMainView.disableLoadBtns()
        self.iMainView.hideReadyLbl()
        self.iMainView.showHandleLbl()
        self.res_sig.connect(self.sig_showFiles)
        thr2 = Thread(target=self.model.startListenFiles, args=(self, self.res_sig, ))
        thr2.start()


class MainView(QtWidgets.QMainWindow, MVtest.Ui_MainWindow, IMainView):

    res_sig = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.presenterMainView = PresenterMainView(self, self.model, self.res_sig)
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
        self.continueBtn.clicked.connect(self.onContinueBtnClicked)
        self.liveListenBtn.clicked.connect(self.onLiveListenBtnClicked)
        self.fileListenBtn.clicked.connect(self.onFileListenBtnClicked)
        self.loadFileBtn.clicked.connect(self.onLoadFileBtnClicked)
        self.checkFileRes.clicked.connect(self.onCheckFileResClicked)

    def onCheckFileResClicked(self):
        self.presenterMainView.checkFilesRes()

    def catalogExecute(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        return dir

    def setResPres(self, resv):
        self.presenterMainView.setResultPres(resv)

    def hideTable(self):
        self.rdBtnTable.hide()
        pass

    def showTable(self):
        self.rdBtnTable.show()
        pass

    def showFileResBtn(self):
        self.checkFileRes.show()
        pass

    def disableLoadBtns(self):
        self.loadBtn.setDisabled(True)
        self.loadFileBtn.setDisabled(True)

    def enableLoadBtns(self):
        self.loadBtn.setDisabled(False)
        self.loadFileBtn.setDisabled(False)

    def onLoadFileBtnClicked(self):
        self.presenterMainView.onLoadFileBtnClicked()

    def onFileListenBtnClicked(self):
        self.presenterMainView.onFileListenBtnClicked()
        self.presenterMainView.saveLang()

    def onLiveListenBtnClicked(self):
        self.presenterMainView.onLiveListenBtnClicked()
        self.presenterMainView.saveLang()

    def showChoiceBtns(self):
        self.liveListenBtn.show()
        self.fileListenBtn.show()

    def hideChoiceBtns(self):
        self.liveListenBtn.hide()
        self.fileListenBtn.hide()

    def unlock(self):
        self.setDisabled(False)

    def getLang(self):
        if self.rusBtn.isChecked():
            return 'rus'
        else:
            return 'eng'

    def closeEvent(self, e):
        self.presenterMainView.stopListen()
        exit(0)

    def onStopClicked(self):
        self.presenterMainView.showResBtn()
        self.presenterMainView.hideBarAndShowBtn()
        self.presenterMainView.moveTime()
        self.presenterMainView.stopTime()
        self.presenterMainView.stopListen()
        self.presenterMainView.stopTimerTag()

    def resumeTimer(self):
        self.timer.start()

    def onContinueBtnClicked(self):
        self.resumeTimer()
        self.presenterMainView.resumeTimerTag()
        self.presenterMainView.resumeListen()
        self.loadBtn.setDisabled(True)
        self.continueBtn.setDisabled(True)
        self.pauseBtn.setDisabled(False)

    def stopTimer(self):
        self.timer.stop()

    def hideRecBtn(self):
        self.recBtn.hide()

    def moveTime(self):
        self.tEdit.setGeometry(430, 410, 131, 31)

    def onPauseClicked(self):
        self.loadBtn.setDisabled(False)
        self.continueBtn.setDisabled(False)
        self.pauseBtn.setDisabled(True)
        self.presenterMainView.stopTimerTag()
        self.presenterMainView.pauseListen()

    def moveLoadBtn(self):
        self.loadBtn.setGeometry(340, 70, 271, 51)

    def showLoadFileBtn(self):
        self.moveLoadBtn()
        self.hideChoiceBtns()
        self.loadFileBtn.setGeometry(340, 140, 271, 51)
        self.loadFileBtn.show()

    def onRecBtnClicked(self):
        self.timer.start()
        self.hideRecBtn()
        self.presenterMainView.timerContinue()
        self.presenterMainView.onRecBtnClicked()
        self.presenterMainView.startListen()
        self.loadBtn.setDisabled(True)
        self.pauseBtn.setDisabled(False)
        self.stopBtn.setDisabled(False)
        self.continueBtn.setDisabled(True)

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

    def hideReadyLbl(self):
        self.readyLbl.hide()

    def showReadyLbl(self):
        self.readyLbl.show()

    def hideHandleLbl(self):
        self.handleLbl.hide()

    def showHandleLbl(self):
        self.handleLbl.show()

    def onViewLoaded(self):
        self.setWindowTitle('Lyrics Listener')
        self.setWindowIcon(QtGui.QIcon('Images/icon_LyrLis.png'))
        self.pauseBtn.setDisabled(True)
        self.stopBtn.setDisabled(True)
        self.continueBtn.setDisabled(True)
        self.fileListenBtn.hide()
        self.loadFileBtn.hide()
        self.liveListenBtn.hide()
        self.hideButtonStartListen()
        self.hideBtnShowResult()
        self.hideCmb()
        self.hideListenBar()
        self.hideTime()
        self.hideTable()
        self.hideHandleLbl()
        self.hideReadyLbl()

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
        self.continueBtn.hide()
        self.stopBtn.hide()

    def hideTime(self):
        self.tEdit.hide()

    def showListenBar(self):
        self.recBtn.show()
        self.pauseBtn.show()
        self.continueBtn.show()
        self.stopBtn.show()
        self.tEdit.show()

    def onLoadBtnClicked(self):
        self.setDisabled(True)
        self.presenterMainView.openLyricsView()
        pass

    def showBtnShowResult(self):
        self.showResBtn.show()

    def hideBtnShowResult(self):
        self.showResBtn.hide()
        self.checkFileRes.hide()

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
        self.presenterMainView.onShowResClicked()
        pass

    def showRes(self, output):
        QtWidgets.QMessageBox.information(self, 'Результат', 'Оценка по десятибальной шкале: '+str(output))