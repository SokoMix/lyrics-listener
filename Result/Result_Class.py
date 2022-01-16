from Result import Result_GUI
from PyQt5 import QtWidgets, QtGui
from abc import ABCMeta, abstractmethod


class iResultView():
    __metaclass__ = ABCMeta

    @abstractmethod
    def showView(self):
        pass

    @abstractmethod
    def hideView(self):
        pass

    @abstractmethod
    def appendText(self, stroka):
        pass

    @abstractmethod
    def clearCmb(self):
        pass


class PresenterResult():
    def __init__(self, iresultview: iResultView, model):
        super().__init__()
        self.iResultView = iresultview
        self.model = model

    def hideView(self):
        self.iResultView.hideView()

    def showView(self):
        self.iResultView.showView()

    def clearCmb(self):
        self.iResultView.clearCmb()

    def showFiles(self):
        self.clearCmb()
        files = self.model.getAudioFiles()
        new_f = ['0']*len(files)
        for i in range(len(files)):
            ind1 = files[i].rfind('/')
            ind2 = files[i].rfind(r"\ "[0])
            mx_ind = max(ind1, ind2)
            new_f[i] = files[i][mx_ind+1:]
        filesRes = self.model.getSimilarity()
        for i in range(len(new_f)):
            self.iResultView.appendText(str(i+1)+'. '+new_f[i]+' - '+str(filesRes[i])+' б.')
        self.showView()



class Result(QtWidgets.QDialog, Result_GUI.Ui_Dialog, iResultView):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.presenterResult = PresenterResult(self, self.model)
        self.setupUi(self)
        self.readyBtn.clicked.connect(self.hideView)
        self.setWindowTitle('Результат проверки')
        self.hide()

    def onReadyBtnClicked(self):
        self.presenterResult.hideView()

    def clearCmb(self):
        self.resTxt.clear()

    def showView(self):
        self.show()

    def givePresenter(self):
        return self.presenterResult

    def hideView(self):
        self.hide()

    def appendText(self, stroka):
        self.resTxt.append(stroka)
