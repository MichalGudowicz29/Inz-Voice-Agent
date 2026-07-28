import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer


q = queue.Queue()

model = Model("models/vosk-model-small-pl-0.22")

recognizer = KaldiRecognizer(
    model,
    16000
)


def callback(indata, frames, time, status):
    q.put(bytes(indata))


with sd.RawInputStream(
    samplerate=16000,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):

    print("Mów...")

    while True:
        data = q.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(
                recognizer.Result()
            )

            print(result["text"])
