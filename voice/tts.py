import sounddevice as sd
import numpy as np
import time 
import queue
import threading
from supertonic import TTS

tts = TTS(auto_download=True)
VOICE_NAME = 'M2'
LANG = 'pl'
TOTAL_STEPS = 8
SPEED = 1.05
SAMPLERATE = 44100
    
# Dodanie watku roboczego, aby speak nigdy nie blokowalo watku z graphem
# konsumuje kolejke po kolei, zeby audio na siebie nie nachodzilo
# top 1 priority zeby graph nie czekal ani sekundy, speak powinno nakladac zerowy delay na graph

_speech_queue: queue.Queue = queue.Queue()


def _playback_worker():
    while True:
        text, style_kwargs = _speech_queue.get()
        try:
            _synthesize_and_play(text, **style_kwargs)
        except Exception as e:
            print(f"[TTS worker] blad: {type(e).__name__}: {e}")
        finally:
            _speech_queue.task_done()


_worker_thread = threading.Thread(target=_playback_worker, daemon=True)
_worker_thread.start()




def _synthesize_and_play(
    text: str,
    voice_name: str = VOICE_NAME,
    lang: str = LANG,
    total_steps: int = TOTAL_STEPS,
    speed: float = SPEED,
    samplerate: int = SAMPLERATE,
):
    """Rzeczywista synteza + odtwarzanie — blokujące, ale wykonywane
    WYŁĄCZNIE wewnątrz wątku roboczego, nigdy w wątku wywołującym."""
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
 
    sd.play(wav, samplerate=samplerate)
    sd.wait()
 
    print(
        f"[TTS worker] generate: {t1 - t0:.3f}s | "
        f"total (gen+play): {time.time() - t0:.3f}s | tekst: {text[:40]!r}"
    )



def speak(
    text: str,
    voice_name: str = VOICE_NAME,
    lang: str = LANG,
    total_steps: int = TOTAL_STEPS,
    speed: float = SPEED,
    samplerate: int = SAMPLERATE,
):
    """Nieblokujące wywołanie — wraca natychmiast, faktyczna praca dzieje się
    w tle. Wywołujący (np. node w LangGraph) może kontynuować dalej (np.
    planner może zacząć liczyć swoje LLM call) podczas gdy audio się gra."""
    _speech_queue.put((
        text,
        {
            "voice_name": voice_name,
            "lang": lang,
            "total_steps": total_steps,
            "speed": speed,
            "samplerate": samplerate,
        },
    ))


def wait_until_speech_done():
    """Opcjonalne: użyj gdy naprawdę potrzebujesz poczekać (np. na sam koniec
    programu przed wyjściem, żeby nie uciąć ostatniego zdania)."""
    _speech_queue.join()
