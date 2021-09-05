import sys
from loadLyrClass import LoadView
from TextCatcherClass import TextCatcher
from MainViewClass import MainView
from PyQt5 import QtWidgets


class Model(object):
    text_lyrics = ''
    text_said = ''

    def __init__(self):
        super().__init__()

    def setTextLyr(self, txt):
        self.text_lyrics = txt


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