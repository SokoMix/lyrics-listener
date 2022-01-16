import sys
from LoadLyrics.LoadLyr_Class import LoadView
from TextCatcher.TextCatcher_Class import TextCatcher
from MainWindow.MainView_Class import MainView
from PyQt5 import QtWidgets
from Result.Result_Class import Result
from Model.Model_Class import Model
try:
    from PyQt5.QtWinExtras import QtWin
    myappid = "SokoMix's project"
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

def main():
    model = Model()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName('Lyrics Listener')
    mainv, loadv, catchtxt, resv = MainView(model), LoadView(model), TextCatcher(model), Result(model)
    mainv.setPres(loadv.givePresenter())
    mainv.setResPres(resv.givePresenter())
    loadv.setPresenterLoadV(catchtxt.givePresenter())
    loadv.setPresenterMainV(mainv.givePresenter())
    catchtxt.setPresenterLoadV(loadv.givePresenter())
    app.exec_()


if __name__ == '__main__':
    main()
