import sounddevice as sd
import numpy as np
import time 
from supertonic import TTS
from queue import Queue
from threading import Thread, Event


tts = TTS(auto_download=True)
VOICE_NAME = 'M2'
LANG = 'pl'
TOTAL_STEPS = 8
SPEED = 1.05
SAMPLERATE = 44100

style= tts.get_voice_style(VOICE_NAME)

speech_queue = Queue()

can_listen = Event()
can_listen.set()

def worker():
    while True:
        text = speech_queue.get()
        can_listen.clear()
        
        try: 
            wav, duration = tts.synthesize(text, style)
            wav = np.squeeze(wav)

            sd.play(wav)
            sd.wait()
        
        finally:
            can_listen.set()
            speech_queue.task_done()

Thread(target=worker, daemon=True).start()

def speak(text):
    speech_queue.put(text)


def wait_until_speech_done():
    speech_queue.join()
