import sys
from threading import Thread
from VoskApi.VoskApi_Class import VoskApi
from pymystem3 import Mystem
sys.path.append('../Lib')
from Lib import cpp_text_check


class Model(object):

    def __init__(self):
        super().__init__()
        self.text_lyrics = ''
        self.text_said = ''
        self.similarity = None
        self.isLisStarted = False
        self.voskApi = None
        self.inputDevices = None
        self.audioFiles = None
        self.lang = None

    def setAudioFiles(self, list):
        self.audioFiles = list

    def getAudioFiles(self):
        return self.audioFiles

    def setLang(self, st):
        self.lang = st

    def getLang(self):
        return self.lang

    def setInputDevices(self, list):
        self.inputDevices = list

    def setTextLyr(self, txt):
        self.text_lyrics = txt

    def setDeviceId(self, id):
        self.voskApi = VoskApi(max(0, self.inputDevices[id - 1]), self.lang, None, self)

    def startListen(self):
        self.isLisStarted = True
        thr1 = Thread(target=self.voskApi.startLisLive, args=())
        thr1.start()

    def startListenFiles(self, mpres, res_sig):
        self.isLisStarted = True
        self.voskApi = VoskApi(0, self.lang, mpres, self)
        self.voskApi.set_PathFiles(self.audioFiles)
        self.voskApi.listenFiles()
        res_sig.emit()

    def checkFilesRes(self):
        self.text_lyrics = self.textHandle(self.text_lyrics)
        data = self.voskApi.get_saidFiles()
        self.similarity = len(data)*[0]
        for i in range(len(data)):
            data[i] = self.textHandle(data[i])
            self.similarity[i] = round(cpp_text_check.checkResult(data[i], self.text_lyrics)*10)

    def pauseListen(self):
        self.voskApi.pause()

    def getSimilarity(self):
        return self.similarity

    def resumeListen(self):
        self.voskApi.resume()

    def stopListen(self):
        if self.isLisStarted:
            self.voskApi.stop()
            self.isLisStarted = False
            self.text_said = self.voskApi.get_said()

    def textHandle(self, st1: str):
        roothandle = Mystem()
        marks = '''!()-[]{};?@#$%:'"\,./^&;*_<>'''
        st1 = st1.lower()
        st1 = st1.replace('!', ' ')
        for el in marks:
            if el in st1:
                st1 = st1.replace(el, ' ')
        st1 = roothandle.lemmatize(st1)[:-1]
        new_st1 = []
        for el in st1:
            if not (' ' in el and el != ''):
                new_st1.append(el)
        return ' '.join(new_st1)

    def checkResult(self):
        self.text_said = self.textHandle(self.text_said)
        self.text_lyrics = self.textHandle(self.text_lyrics)
        self.similarity = round(cpp_text_check.checkResult(self.text_said, self.text_lyrics)*10)
