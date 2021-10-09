import sys
from loadLyrClass import LoadView
from TextCatcherClass import TextCatcher
from MainViewClass import MainView
from PyQt5 import QtWidgets
from VoskApiClass import VoskApi
from threading import Thread
# import asyncio


isStop = True
isPause = False


class Model(object):

    text_lyrics = ''
    text_said = ''

    def __init__(self):
        super().__init__()

    def setTextLyr(self, txt):
        self.text_lyrics = txt

    def setDeviceId(self, id):
        self.voskApi = VoskApi(max(0, id-1))

    def startListen(self):
        self.text_said = self.voskApi.startLis()

    def pauseListen(self):
        self.voskApi.pause()

    def resumeListen(self):
        self.voskApi.resume()

    def stopListen(self):
        self.voskApi.stop()


def tst():
    i = int(input())
    while i!=3:
        i=int(input())
    print("success")


def main():
    model = Model()
    app = QtWidgets.QApplication(sys.argv)
    mainv, loadv, catchtxt = MainView(model), LoadView(model), TextCatcher(model)
    mainv.setPres(loadv.givePresenter())
    loadv.setPresenterLoadV(catchtxt.givePresenter())
    loadv.setPresenterMainV(mainv.givePresenter())
    catchtxt.setPresenterLoadV(loadv.givePresenter())
    # thread1 = Thread(target=model.startListen, args=())
    # thread1.start()
    app.exec_()


if __name__ == '__main__':
    main()