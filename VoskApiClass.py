import vosk
import queue
import json
import sounddevice
import threading


class VoskApi:

    id = 0

    def __init__(self, device_id):
        super().__init__()
        self.id = device_id
        pass

    def stop(self):
        global isStop
        isStop = True
        pass

    def pause(self):
        global isPause
        isPause = True

    def resume(self):
        global isPause
        isPause = False

    def get_said(self):
        return self.said

    def set_deviceid(self, id):
        self.id = id

    def startLis(self):
        q = queue.Queue()
        global isStop
        global isPause
        isStop = False
        isPause = False
        self.said = ''
        samplerate = int(sounddevice.query_devices(self.id, 'input')['default_samplerate'])
        model = vosk.Model(r"vosk-model-small-ru-0.15")
        with sounddevice.RawInputStream(samplerate=samplerate, blocksize=16000, device=self.id, dtype='int16', channels=1,
                               callback=(lambda i, f, t, s: q.put(bytes(i)))):
            rec = vosk.KaldiRecognizer(model, samplerate)
            while threading.active_count()==2:
                while not isStop:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        data = json.loads(rec.Result())["text"]
                        if not isPause:
                            self.said += data+' '
                            print(data)
                if isStop:
                    print(self.said)
                    return self.said
        pass
