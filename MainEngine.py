import sys
from LoadLyrics.LoadLyr_Class import LoadView
from TextCatcher.TextCatcher_Class import TextCatcher
from MainWindow.MainView_Class import MainView
from PyQt5 import QtWidgets
from Model.Model_Class import Model

def main():
    model = Model()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName('Lyrics Listener')
    mainv, loadv, catchtxt = MainView(model), LoadView(model), TextCatcher(model)
    mainv.setPres(loadv.givePresenter())
    loadv.setPresenterLoadV(catchtxt.givePresenter())
    loadv.setPresenterMainV(mainv.givePresenter())
    catchtxt.setPresenterLoadV(loadv.givePresenter())
    app.exec_()


if __name__ == '__main__':
    main()
