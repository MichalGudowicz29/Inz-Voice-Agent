22.07.2026
1. Wyszukiwanie geodata na podstawie samego miasta.
2. Sprawdzanie pogody na podstawie geodata.

27.07.2026 
1. Ustalenie architektury rozpisana i rozrysowana w notatniku
2. System prompt i response structure dla agenta Router. 

28.07.2026
1. Ze wzgledu na to ze nie 6.7 sekundy transkrybcji na whisper large turbo jest zdecydowanie za duzo, przechodze na testowanie modelu nastawiony na polski jezyk: vosk-model-small-pl-0.22, jedyne co mnie martwi to 18.36% WER tego modelu, ale licze ze intent accuracy wykaze sie duze, obecna funkcje listen() zostawie poniewaz moze byc ona potrzeba, gdybym chcial pomyslec nad architektura w ktorej samo ASR wykonuje sie adaptacyjnie w zaleznosci od sytuacji. Trzeba mowic wyraznie ale na ten moment jest okej.
2. Dodalem glowna petle w 'main.py', ktora opiera sie na przyjmowaniu wiadomosci z funkcji light_listen(), ktora dziala w tle w zapetleniu, dodalem do niej rowniez mechanizm sprawdzania czy tekst rozni sie od poprzedniego poniewaz bez tego caly czas robil invoke na tej samej wiadomosci. 
3. Przenioslem prompty do pliku prompts.py, agentow do pliku agents.py, a narzedzia do pliku tools.py 
4. Dodalem router, ktory zwraca wedlug response format. need_plan: bool, oraz resoning, dzieki czemu wiemy czy czy trzeba rozpoczac planowanie czy wystarczy odpowiedziec uzytkownikowi, zastanawiam sie czy agent konwersacyjny w ogole jest potrzebny co jezeli router jest w stanie odpowiedziec na pytanie. 
- [x] Dodac agenta konwersacyjnego i planner i zobaczyc ile czasu to wszystko zajmuje i ile tokenow 
5. Agent konwersacyjny jest dodany wraz z promptem, 
6. Dodalem prompt TTS_PROMPT, ktory co do zalozenia ma wymuszac na modelach formatowanie odpowiedzi w sposob latwy do przeczytania dal modelu tts. 
7. poprawka w prompcie routera, poniewaz gdy pytam go co mam zrobic nawet w emocjonalnych sprawach nie chce odpowiadac konkretnie tylko mysli ze odpowiedz wymaga planowania
8. Poprawa Checkpointera aby mogl wywolywac customowe moduly z pamieci takie jak RouterOuput
9. Router dziala, przetestowany, na casualowej rozmowie, gdy poprosilem o wykonanie wyszukania w internecie proba wywolania planner
- [ ] Dodac agenta plannera 
- [ ] Dodac TTS na koncowej odpowiedzi



29.07.2026

