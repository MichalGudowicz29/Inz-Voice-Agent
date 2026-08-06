import pyaudio
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import webrtcvad
import numpy as np
from faster_whisper import WhisperModel
import json
import time 
from voice.tts import can_listen

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE * 0.03) 
SILENCE_LIMIT = 15 
MIN_SPEECH_DURATION = 16 


# heavy listen on macos m2, 6.7s for 2s audio, even on small whisper it gets down to 5.6s.
def listen(
    format: int = FORMAT,
    channels: int = CHANNELS,
    rate: int = RATE,
    chunk: int = CHUNK,
    #transcribe params
    transcribe_model: str = 'small',
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
    vad = webrtcvad.Vad(2)

    buffer = []
    silence_counter = 0

    print("Slucham...")

    try: 
        while True:
            can_listen.wait()
            # pobieramy jedna ramke 30 ms, poniewaz w chunk jest ustawione 0.03, pcm to pulse data modulation
            pcm_data = stream.read(chunk, exception_on_overflow=False)
            #sprawdzamy czy ten chunk jest glosem czy cisza 
            is_speach = vad.is_speech(pcm_data, rate)
            

            if is_speach:
                #jezeli jest mowione to wrzucamy do buffora 
                buffer.append(pcm_data)
                silence_counter = 0
                #print("speach is true")
            else: 
                silence_counter += 1
                #print(f'silence count = {silence_counter}')

                #jezeli przekraczamy limit ciszy co oznacza koniec zdania
                if silence_counter >= SILENCE_LIMIT:
                    # to sprawdzamy czy mamy cos w buferze
                    if buffer:
                        #print('jest bufor')
                        # jezeli mamy i jest to dluzsze niz ustalony prog
                        if len(buffer) < MIN_SPEECH_DURATION:
                            buffer=[]
                            pass 
                        else:
                            rejected: bool = False
                            reason: str = ""
                            # to robimy zamiane na wartosci gotowe do transkrybcji
                            #print('zaczynam transkrybcje')
                            start = time.time()
                            raw_audio = b''.join(buffer)
                            audio_np = np.frombuffer(raw_audio, dtype=np.int16)
                            audio_float = audio_np.astype(np.float32) / 32768.0
                            print(f"Audio length: {len(audio_float)/16000:.2f}s")
                            t0 = time.time()
                            # i odpalamy transkrybcje
                            segments, info = model.transcribe(
                                audio_float,
                                beam_size=1,
                                language='pl',
                                initial_prompt=None
                            )
                            #print(f"[Whisper info] {info}")
                            segments = list(segments)
                            
                            for segment in segments:
                                if segment.avg_logprob < -1.0:
                                    rejected = True
                                    reason = "low_logprob"
                                    break

                                if segment.no_speech_prob > 0.45:
                                    rejected = True
                                    reason = "no_speech"
                                    break

                                if segment.compression_ratio > 2.4:
                                    rejected = True
                                    reason = "compression"
                                    break

                            if rejected:
                                buffer = []
                                silence_counter = 0
                                yield None, 0, reason 
                                continue
                                #print("text:", segment.text)
                                #print("avg_logprob:", segment.avg_logprob)
                                #print("no_speech_prob:", segment.no_speech_prob)
                                #print("compression_ratio:", segment.compression_ratio)


                            t1 = time.time()
                            print(f"Whisper: {t1-t0:.2f}s")
                        # wrzucamy wszystko do zmiennej text
                            #print('jestesmy po transkrybcji')     
                            text = "".join(segment.text for segment in segments).strip()
                            buffer = []
                            print(text)
                            silence_counter=0
                            if text:
                                #print('zwracam tekst')
                                end=time.time()
                                delay= end-start
                                #print(f'inside func: {text}')
                                yield text, delay, None
                            else:
                                #print('nie ma zwrotu robie continue')
                                continue
                        silence_counter = 0 
    except Exception as e:
        return f'{type(e).__name__}: {e}'

def light_listen():
    t0 = time.time()

    q = queue.Queue()

    model = Model("models/vosk-model-small-pl-0.22")

    t1 = time.time()
    print(f"[ASR] Model load time: {t1 - t0:.3f}s")

    recognizer = KaldiRecognizer(
        model,
        16000
    )

    def callback(indata, frames, time, status):
        q.put(bytes(indata))


    with sd.RawInputStream(
        samplerate=16000,
        blocksize=1600,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        print("Light listen activated...")

        last_text = ""

        while True:
            # czas oczekiwania na audio
            t_wait_start = time.time()

            data = q.get()

            t_wait_end = time.time()

            # czas samego Vosk
            t_vosk_start = time.time()

            if recognizer.AcceptWaveform(data):
                result = json.loads(
                    recognizer.Result()
                )

                text = result["text"].strip()

                t_vosk_end = time.time()

                if text and text != last_text:
                    last_text = text

                    print(
                        f"[ASR] Wait audio: {t_vosk_start - t_wait_start:.3f}s"
                    )

                    print(
                        f"[ASR] Vosk processing: {t_vosk_end - t_vosk_start:.3f}s"
                    )

                    print(
                        f"[ASR] Total recognition: {t_vosk_end - t_wait_start:.3f}s"
                    )

                    print(
                        f"[ASR] Text: {text}"
                    )

                    yield text
