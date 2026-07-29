import sounddevice as sd
import numpy as np
import time 
from supertonic import TTS

tts = TTS(auto_download=True)
VOICE_NAME = 'M2'
LANG = 'pl'
TOTAL_STEPS = 8
SPEED = 1.05
SAMPLERATE = 44100
     
def speak(
    text: str,
    tts: TTS = tts,
    voice_name: str = VOICE_NAME,
    lang: str = LANG,
    total_steps: int = TOTAL_STEPS,
    speed: float = SPEED,
    samplerate: int = SAMPLERATE

):
    t0 = time.time()
    style = tts.get_voice_style(voice_name=voice_name)

    wav, duration = tts.synthesize(
        text=text,
        lang=lang,
        voice_style=style,
        total_steps=total_steps,
        speed=speed,
    )

    t1 = time.time()

    wav = np.squeeze(wav)

    t2 = time.time()

    sd.play(
        wav,
        samplerate=samplerate
    )
    
    t3 = time.time()

    sd.wait()

    print(
        f"TTS generate: {t1-t0:.3f}s | "
        f"play start: {t2-t1:.3f}s | "
        f"full audio: {t3-t0:.3f}s"
    )
