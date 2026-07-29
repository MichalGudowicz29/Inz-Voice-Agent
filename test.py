from supertonic import TTS
import sounddevice as sd
import numpy as np


tts = TTS(auto_download=True)

style = tts.get_voice_style(voice_name="M2")

text = """
Cześć Marek.
To jest test Supertonic 3 uruchomiony lokalnie.
"""


wav, duration = tts.synthesize(
    text=text,
    lang="pl",                          
    voice_style=style,              # Voice style object
    total_steps=8,                  # Quality: 5 (low) to 12 (high), default 8 (medium)
    speed=1.05,                     # Speed: 0.7 (slow) to 2.0 (fast)
)

wav = np.squeeze(wav)

sd.play(
    wav,
    samplerate=44100
)

sd.wait()

