# Inz-Voice-Agent

**Inz-Voice-Agent** to asystent głosowy zbudowany w Pythonie, oparty o architekturę multi-agentową i LangGraph.  
Projekt łączy rozpoznawanie mowy, generowanie odpowiedzi, planowanie zadań oraz syntezę mowy, aby umożliwić naturalną interakcję głosową z użytkownikiem.



## Opis projektu

System działa jako pipeline kilku współpracujących ze sobą agentów:

- **ASR (Automatic Speech Recognition)** – rozpoznaje mowę użytkownika
- **Assistant** – decyduje, czy wystarczy zwykła odpowiedź, czy trzeba uruchomić planowanie
- **Planner** – rozbija bardziej złożone zadanie na kroki
- **Verifier** – sprawdza, czy plan jest poprawny i wykonalny
- **Executor** – wykonuje zaakceptowany plan
- **Synthesizer** – przygotowuje krótką, naturalną odpowiedź końcową
- **TTS (Text to Speech)** – zamienia odpowiedź na mowę

Projekt został zaprojektowany tak, aby wspierać bardziej złożone zadania głosowe niż zwykły chatbot, np. planowanie, wyszukiwanie informacji czy obsługę zapytań wymagających użycia narzędzi.

## Najważniejsze funkcje

- obsługa komunikacji głosowej
- rozpoznawanie mowy użytkownika
- automatyczne planowanie zadań przez agenta
- weryfikacja poprawności planu przed wykonaniem
- korzystanie z narzędzi zewnętrznych, np. wyszukiwania i pogody
- synteza krótkich odpowiedzi głosowych
- architektura oparta o LangGraph

## Technologie

- **Python**
- **LangGraph**
- **LangChain**
- **OpenAI / modele LLM**
- **Whisper / Faster Whisper**
- **Vosk**
- **PyAudio**
- **sounddevice**
- **webrtcvad**

## Architektura

![Architektura systemu](agent_graph.png)

Projekt wykorzystuje graf stanów, w którym kolejne nody odpowiadają za różne etapy przetwarzania:

1. odebranie głosu od użytkownika
2. transkrypcję tekstu
3. analizę intencji
4. ewentualne planowanie zadania
5. weryfikację planu
6. wykonanie kroków
7. wygenerowanie końcowej odpowiedzi
8. odczytanie odpowiedzi głosem

W repozytorium znajdują się również diagramy i przykłady działania w katalogu `docs/demo/`.

## Struktura projektu

- `main.py` – główna pętla aplikacji
- `graph/` – definicja grafu LangGraph oraz stanów
- `agents/` – logika agentów
- `prompts/` – prompty używane przez modele
- `tools/` – narzędzia wykorzystywane przez agentów
- `voice/` – rozpoznawanie i synteza mowy
- `docs/` – dokumentacja i materiały pomocnicze

## Uruchomienie

1. Skonfiguruj zmienne środowiskowe w pliku `.env`
2. Uruchom aplikację:

```bash
langgraph dev

