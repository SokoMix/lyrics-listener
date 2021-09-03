import sys
import mainwindow
import loadLyrics
import enterLyrics
from PyQt5 import QtWidgets
from abc import ABCMeta, abstractmethod, abstractproperty


class Model(object):
    text_lyrics = ''
    text_said = ''

    def __init__(self):
        super().__init__()

    def setTextLyr(self, txt):
        self.text_lyrics = txt


class ITextCatcher():
    __metaclass__ = ABCMeta
    def __init__(self):
        super().__init__()

    @abstractmethod
    def showView(self):
        pass

    @abstractmethod
    def givePresenter(self):
        pass


class PresenterTextCatcher():
    def __init__(self, itextcatcher, model : Model):
        super().__init__()
        self.iTextCatcher = itextcatcher
        self.model = model
        self.presenterLoadView = None

    def setPresLoadV(self, pres):
        self.presenterLoadView = pres

    def showBtn(self):
        self.presenterLoadView.showBtn()


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

    def setModelTxt(self, txt):
        pass


class PresenterLoadView():
    def __init__(self, iloadview, model : Model):
        super().__init__()
        self.model = model
        self.iLoadView = iloadview
        self.presenterTextCatcher = None
        self.presenterMainV = None

    def setPresenterTextCatcher(self, pres):
        self.presenterTextCatcher = pres

    def setpresenterMainV(self, pres):
        self.presenterMainV = pres

    def showBtn(self):
        self.presenterMainV.showBtn()

    def openTextCatcher(self):
        self.presenterTextCatcher.iTextCatcher.showView()

    def hideView(self):
        self.iLoadView.hideView()


class IMainView():
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def showListenBtn(self):
        pass

    def loadBtn(self):
        pass

    def startListBtn(self):
        pass

    def showRes(self):
        pass

    def showListenBar(self):
        pass

    def hideButtons(self):
        pass

    def setPres(self, pres):
        pass


class PresenterMainView():
    def __init__(self, imainview, model : Model):
        super().__init__()
        self.model = model
        self.iMainView = imainview
        self.presenterLoadView = None

    def setPresenterLoad(self, presenter : PresenterLoadView):
        self.presenterLoadView = presenter

    def openLyricsView(self):
        self.presenterLoadView.iLoadView.showView()

    def showBtn(self):
        self.iMainView.showListenBtn()



class MainView(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow, IMainView):
    def __init__(self, model : Model):
        super().__init__()
        self.model = model
        self.presenterMainView = PresenterMainView(self, self.model)
        self.setupUi(self)
        self.setWindowTitle('Проверить стих')
        self.show()
        self.hideButtons()
        self.pushButton.clicked.connect(self.loadBtn)
        self.pushButton_2.clicked.connect(self.startListBtn)
        self.pushButton_3.clicked.connect(self.showRes)

    def showListenBtn(self):
        if not self.pushButton_4.isVisible():
            self.pushButton_2.show()

    def setPres(self, pres):
        self.presenterMainView.setPresenterLoad(pres)

    def hideButtons(self):
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.timeEdit.hide()

    def showListenBar(self):
        self.pushButton_2.hide()
        self.pushButton_4.show()
        self.pushButton_5.show()
        self.pushButton_6.show()
        self.pushButton_7.show()
        self.timeEdit.show()

    def loadBtn(self):
        self.presenterMainView.openLyricsView()
        pass

    def startListBtn(self):
        self.showListenBar()

        self.pushButton_3.show()
        pass

    def givePresenter(self):
        return self.presenterMainView

    def showRes(self):
        pass


class LoadView(QtWidgets.QDialog, loadLyrics.Ui_Dialog, ILoadView):
    def __init__(self, model : Model):
        super().__init__()
        self.model = model
        self.setupUi(self)
        self.setWindowTitle('Загрузить стих')
        self.hide()
        self.presenterLoadView = PresenterLoadView(self, self.model)
        self.pushButton_2.clicked.connect(self.loadFile)
        self.pushButton.clicked.connect(self.loadText)

    def setModelTxt(self, txt):
        self.model.setTextLyr(txt)

    def loadText(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Text Files(*.txt)")
        text = ''
        if filename != '':
            with open(filename, 'r') as f:
                text = f.read()
            text = text.replace('\n', ' ')
            self.setModelTxt(text)
            self.hideView()
            self.presenterLoadView.showBtn()
        pass

    def hideView(self):
        self.hide()

    def setPresenterLoadV(self, pres):
        self.presenterLoadView.setPresenterTextCatcher(pres)

    def loadFile(self):
        self.presenterLoadView.openTextCatcher()
        pass

    def setPresenterMainV(self, pres):
        self.presenterLoadView.setpresenterMainV(pres)
        pass

    def givePresenter(self):
        return self.presenterLoadView

    def showView(self):
        self.show()


class TextCatcher(QtWidgets.QDialog, enterLyrics.Ui_Dialog, ITextCatcher):
    def __init__(self, model : Model):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Введите текст')
        self.model = model
        self.presenterTextCatcher = PresenterTextCatcher(self, model)
        self.hide()
        self.pushButton.clicked.connect(self.readyBtn)

    def showView(self):
        self.show()

    def hideView(self):
        self.hide()

    def givePresenter(self):
        return self.presenterTextCatcher

    def setPresenterLoadV(self, pres):
        self.presenterTextCatcher.setPresLoadV(pres)

    def readyBtn(self):
        txt = self.textEdit.toPlainText()
        if txt != '':
            self.model.setTextLyr(txt.replace('\n', ' '))
            self.hideView()
            self.presenterTextCatcher.presenterLoadView.hideView()
            self.presenterTextCatcher.showBtn()
        else:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введите текст', QtWidgets.QMessageBox.Ok)
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    mainv, loadv, catchtxt = MainView(model), LoadView(model), TextCatcher(model)
    mainv.setPres(loadv.givePresenter())
    loadv.setPresenterLoadV(catchtxt.givePresenter())
    loadv.setPresenterMainV(mainv.givePresenter())
    catchtxt.setPresenterLoadV(loadv.givePresenter())
    app.exec_()


if __name__ == '__main__':
    main()