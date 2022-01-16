import vosk
import queue
import json
import sounddevice
import wave


class PresenterVoskApi():

    def __init__(self, mpres, model):
        super().__init__()
        self.mainViewPresenter = mpres
        self.model = model

    def finishHandleFiles(self):
        self.mainViewPresenter.finishHandle()
        self.model.checkFilesRes()

class VoskApi:

    id = 0
    isPause = False
    isStop = False
    pathFiles = None
    said = ''
    saidFiles = ''

    def __init__(self, device_id, lang, mpres, model):
        super().__init__()
        self.lang = lang
        self.voskPresenter = PresenterVoskApi(mpres, model)
        self.id = device_id
        self.model = vosk.Model(r'VoskApi/vosk-model-en') if lang == 'eng' else vosk.Model(r'VoskApi/vosk-model-ru')
        pass

    def stop(self):
        self.isStop = True
        pass

    def set_PathFiles(self, paths):
        self.pathFiles = paths

    def pause(self):
        self.isPause = True

    def resume(self):
        self.isPause = False

    def get_said(self):
        return self.said

    def set_deviceid(self, id):
        self.id = id

    def set_saidFiles(self, saidFiles):
        self.saidFiles = saidFiles

    def get_saidFiles(self):
        return self.saidFiles

    def listenFiles(self):
        saidFiles = len(self.pathFiles) * ['']
        rec = vosk.KaldiRecognizer(self.model, 32000)
        for i in range(len(self.pathFiles)):
            wv = wave.open(self.pathFiles[i], 'rb')
            lyr = ''
            data ='no'
            while len(data)!=0:
                data = wv.readframes(32000)
                print(lyr)
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    if res['text'] != '':
                        lyr += res['text'] + ' '
            res = json.loads(rec.FinalResult())
            saidFiles[i] =lyr + res['text']
            wv.close()
        self.set_saidFiles(saidFiles)
        self.voskPresenter.finishHandleFiles()

    def startLisLive(self):
        q = queue.Queue()
        self.isStop = False
        self.isPause = False
        self.said = ''
        samplerate = int(sounddevice.query_devices(self.id, 'input')['default_samplerate'])
        with sounddevice.RawInputStream(samplerate=samplerate, blocksize=16000, device=self.id, dtype='int16', channels=1,
                               callback=(lambda i, f, t, s: q.put(bytes(i)))):
            rec = vosk.KaldiRecognizer(self.model, samplerate)
            while not self.isStop:
                data = q.get()
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.Result())["text"]
                    if not self.isPause:
                        self.said += data+' '
                    print(self.said)
        pass