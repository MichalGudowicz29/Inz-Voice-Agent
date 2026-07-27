import pyaudio
import webrtcvad
import numpy as np
from faster_whisper import WhisperModel
import json
import requests
import time 

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE * 0.03) 
SILENCE_LIMIT = 15 
MIN_SPEECH_DURATION = 16 



def listen(
    format: int = FORMAT,
    channels: int = CHANNELS,
    rate: int = RATE,
    chunk: int = CHUNK,
    #transcribe params
    transcribe_model: str = 'small-v3-turbo',
    device: str = 'cpu',
    compute_type: str = 'int8'
):
    """
    Args:
        format: format of audio, default paInt16 16 bitowa calkowita 
        channels: 1 for mono, 2 for stereo
        rate: refresh rate domyslnie 16 kHz, probkowanie dzwieku na cyfrowy, 16000 razy na sekunde
    """

    model = WhisperModel(transcribe_model, device=device, compute_type=compute_type)

    # tutaj audio to nasz mikrofon nie przechwytuje ale tworzymy miejsce ktore bedzie
    audio = pyaudio.PyAudio()
    # tutaj dopiero przechwytujemy, input true bo chcemy nagrywac nie odtwarzac
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    # a tutaj sprawdzamy czy ktos mowi czy jest cisza, 3 to wartosc jak agresywnie sprawdzamy 3 to bardzo agresywny 0 to lagodny, agresywny oznacza ze jezeli nie jestem pewien to uznaje to jako cisze 
    vad = webrtcvad.Vad(3)

    buffer = []
    silence_counter = 0

    try: 
        while True:
            # pobieramy jedna ramke 30 ms, poniewaz w chunk jest ustawione 0.03, pcm to pulse data modulation
            pcm_data = stream.read(chunk, exception_on_overflow=False)
            #sprawdzamy czy ten chunk jest glosem czy cisza 
            is_speach = vad.is_speech(pcm_data, rate)


            if is_speach:
                #jezeli jest mowione to wrzucamy do buffora 
                buffer.append(pcm_data)
                silence_counter = 0
                print("speach is true")
            else: 
                silence_counter += 1
                print(f'silence count = {silence_counter}')

                #jezeli przekraczamy limit ciszy co oznacza koniec zdania
                if silence_counter >= SILENCE_LIMIT:
                    # to sprawdzamy czy mamy cos w buferze
                    if buffer:
                        print('jest bufor')
                        # jezeli mamy i jest to dluzsze niz ustalony prog
                        if len(buffer) < MIN_SPEECH_DURATION:
                           pass 
                        else:
                            # to robimy zamiane na wartosci gotowe do transkrybcji
                            print('zaczynam transkrybcje')
                            start = time.time()
                            raw_audio = b''.join(buffer)
                            audio_np = np.frombuffer(raw_audio, dtype=np.int16)
                            audio_float = audio_np.astype(np.float32) / 32768.0
                            # i odpalamy transkrybcje
                            segments, info = whisper_model.transcribe(
                                audio_float,
                                beam_size=5,
                                language='pl',
                                initial_prompt='Język polski. Znaki interpunkcyjne.'
                            )
                        # wrzucamy wszystko do zmiennej text
                            print('jestesmy po transkrybcji')
                            text = "".join([segment.text for segment in segments]).strip()
                            buffer = []
                            print(text)
                            silence_counter=0
                            if text:
                                print('zwracam tekst')
                                end=time.time()
                                delay= end-start
                                print(f'inside func: {text}')
                                yield text, delay
                            else:
                                print('nie ma zwrotu robie continue')
                                continue
                        silence_counter = 0 
    except Exception as e:
        return f'{type(e).__name__}: {e}'

     
def speak():
        pass


if (__name__=='__main__'):
    print("Ładowanie modelu Whisper (może chwilę potrwać przy pierwszym uruchomieniu)...")
    whisper_model = init_transcribe_model()
    print("Model załadowany.")
 
    for text, delay in listen(model=whisper_model):
        print(f"[{delay:.2f}s] Rozpoznano: {text}")
