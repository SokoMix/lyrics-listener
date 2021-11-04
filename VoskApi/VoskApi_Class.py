import vosk
import queue
import json
import sounddevice


class VoskApi:

    id = 0
    isPause = False
    isStop = False
    said = ''

    def __init__(self, device_id):
        super().__init__()
        self.id = device_id
        pass

    def stop(self):
        self.isStop = True
        pass

    def pause(self):
        self.isPause = True

    def resume(self):
        self.isPause = False

    def get_said(self):
        return self.said

    def set_deviceid(self, id):
        self.id = id

    def startLis(self):
        q = queue.Queue()
        self.isStop = False
        self.isPause = False
        self.said = ''
        samplerate = int(sounddevice.query_devices(self.id, 'input')['default_samplerate'])
        model = vosk.Model(r"VoskApi/vosk-model-ru-0.10")
        with sounddevice.RawInputStream(samplerate=samplerate, blocksize=16000, device=self.id, dtype='int16', channels=1,
                               callback=(lambda i, f, t, s: q.put(bytes(i)))):
            rec = vosk.KaldiRecognizer(model, samplerate)
            while not self.isStop:
                data = q.get()
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.Result())["text"]
                    if not self.isPause:
                        self.said += data+' '
                    print(self.said)
        pass