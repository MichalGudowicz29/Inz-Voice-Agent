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
1. Problem z dobraniem polskiego modelu TTS polega na tym ze duzo popularnych dobrze dostrojonych modeli bazuje na architekturze StyleTTS2, ktory ma zaszyty phonemizer espeak-ng i wagi wytrenowane tylko na fonemach z dostepnych jezykow, model po prostu nie widzialp polskich glosek.
2. Okej, znalazlem model nazywa sie SupersonicTTS, wspiera on jezyk polski ale projekt sam w sobie zostaje porzucony z dniem 23 lipca 2026 roku przez co nie chce na nim opierac inzynierki jako ze stracil wsparcie, moim planem jest zrobic fork tego modelu dostroic go jeszcze bardziej na jezyk polski przy pomocy datasetu    Thomcles/YodaLingua-Polish i uzywac go jako glowny model TTS, uwazam ze model TTS jest na tyle istnotny w projekcie jako ze jest to modul ktory najczesciej spotyka sie z opinia uzytkownika 
### Problem badawczy
3. Fine tuning to fajny aspekt badawczy i na pewno do zrobienia jako ze jest juz kod supertonic-pytorch ktory dzieki reverse engineering modelu onnx, przedstawia pipeline do fine tuningu supertonic tts v2, a my chcemy v3, wiec wezme kod supertonic-pytorch, przeroobie go na pipeline pod trenowanie trzeciej wersji, i nastepnie przetrenuje go dokladniej pod polski jezyk.  
4. Dziala wystarczajaco dobrze ten model supertonic3 po testach, nie przejmowalbym sie na razie fine tuningiem, tym czym bym sie martwil to 
    1. Dlugi czas od powiedzenia slowa, do uslyszenia odpowiedzi, to sie jakos nazywalo ale jest to za dlugie 
    2. Zdecydowanie trzeba zamienic invoke na streaming 

### Plan do przetestowania
Zamiast mowa -> invoke modelu -> odpowiedz modelu do TTS -> czytanie odpowiedzi, to przechwytywanie tego co mowi uzytkownik w calosci, i potem dajemy to do modelu i zmieniamy invoke na streaming, i te streamowane chunki od razu przekazujemy do mowy, przez co mowimy od razu to co dostaniemy a nie czekamy na cala odpowiedz, i potem porownac czasy 
Problemem jest czas
Overall time: 25.426538944244385 s

router invoke
ri: 6.218886137008667 s

conversational invoke
ci: 11.338120937347412 s

speaking time
sp: 7.869211196899414 s

to sa obecne czasy zdecydowanie za dlugie, 17 sekund na sama logike agentow gdzie konwersacja z uzytkonwikiem ma na to maksymalnie 2 sekundy, to jest 15 sekund do zbicia. 

1. Zmienilem modele na gpt 4o mini zeby router i conversational byly lekkie i nie robimy reasoningu niepotrzebnie duzego, docelowo nawet mniejsze moglyby byc te modele, za to planner bylby wtedy ciezszy
2. problem 1 sekundowe opoznineie w speak()
3. Czytanie summarize middleware message
czasy po poprawce zmiana model na mniejszy i streaming odpowiedzi do speak

Time to First Audio: 0.71s

TTS generate: 0.966s | play start: 0.000s | full audio: 0.971s

Overall time: 8.20383596420288 s

router invoke
ri: 2.2742910385131836 s

conversational invoke
ci: 5.9294562339782715 s

warto sprobowac co sie stanie gdy zmniejszymy total steps w speka z 8 na 5 wedlug dokumentacji supertonic zmiejszy to jakosc ale zwiekszy predkosc


4. Duzym problem jest router, ponad 2 sekundy. Problemem moze byc to ze jest to agent, tworzy sie agent loop dostaje ogromny kontekst historie i przepala mase tokenow, zamiast tego bedzie po prostu wywolaniem modelu. zobaczymy ile to pomoze
5. Czasowo pomaga ale problem jest inny, teraz gdy konwersator i router nie sa agentami to trace przywilej tworzenia historii automatycznie poprzez langgraph, teraz musze stworzyc klase state, graph i graph compile zeby historia sama sie dopisywala, zobaczymy czy bez agenta ale z reczna historia zyskam na czasie.
6. Przeszedlem z langchain i create agent do langgraph i stworzylem graph gdzie node to agenci a edges to polaczenia miedzy nimi, dzieki czemu licze ze zyskam troche czasu, ale na pewno daje to wieksza elastycznosc.
7. Na razie usuwam ale docelowo trzeba wprowadzic middleware z summarize model
8. Nie pomoglo, zmienilem na langgraph i mam wieksza kontrole nad wywolaniem ale dalej 7 sekund do pierwszego tokenu gdzie 3 sekundy routera to zdecydowanie za dlugo. 

9. Ustaiwnie modeli na 4o mini z reasoning effort minimal dalo duzo lepsze wyniki, wszystko jest w langgraphie a funkcje wywoluje bezposrednio model z historia bez calej otoczki create_agent
10. Troche zamieszania z architektura, zostane przy langgraph juz przyszlosciowo ale musze uporzadkowac kod, przy testowaniu modelu tts duzo sie nabalaganilo

11. okej jest w miare porzadek, dalej denerwuje mnie ten router 1.6 sekundy i to ze lacznie czeka sie okolo 4 sekundy na audio 

- [x] Poprawic czas do pierwszego audio 
- [ ] Dodac planner node ktory bedzie w stanie wywolac agenta planuajcego
- [x] Poprawic problem jest taki ze gdy node routera zaczyna to sprawdza czy need plan jest true, ale problem jest w tym ze nigdy nie zmieniamy wartosci tego na True albo False poniewaz nasz conversational agent tylko czyta i wywoluje konwersacje a powinien jeszcze sprawdzac stan i go zmieniac

Okej wszystko jest na ten moment moim zdaniem w porzadku oprocz
1. zbyt robotyczny glos
2. calkiem dlugo mieli TTS, ale to sie przetestuje na mocniejszym komputerze

Teraz mozna isc w tworzenie odnogi plannera, weryfikator i tak dalej, zeby mogl wykonywac mocniejsze zadania, 

zalozenie jest takie 
Planner dostaje zadanie, uklada plan jak je wykonac, nastepnie do weryfikatora, nastepnie do wykonawcy, wykonawca wykonuje np. tool1 tool2 tool3, potem jest synchronizator, ktory dostaje odpowiedzi z toolsow, plan i weryfikacje i scala to w odpowiedz, nastepnie wyjscie z tego to jest wykonanie zadania 

na ten moment agent traktuje plannera jako osobe ktora ma cos zaplanowac np. wesele, to jest wina promptu trzeba go zmienic na to aby wiedzial ze planner jest od wykonania zadania ktore jest poza jego zasiegiem np. 

User; zaplanuj mi wesele 
agent asystent powinien przeslac zadanie do planner, nastepnie planner powinien ulozyc plan czego bedzie potrzebowal np. 
1. Miejsce na wesele 
2. Dojazd
weryfikator powiedzial okej faktycznie mamy takie toolsy jestesmy w stanie to wykonac
wykonawca szuka w internecie, sprawdza dojazd na pkp api, 
synchronizator bierze wszystkie informacje spaja to i daje koncowa odpowiedz

w kazdym momencie gdzie czegos brakuje agent powinien zawiesic swoje dzialanie i dopytac np. okej a w jakim miejscu chcesz to wesele, zapytac i potem wrocic do planowania - to moze byc ciezkie 

plan na jutro to usiasc do tego plannera
dodac tts jako node

## wazne  
agenci to po prostu autonomiczne jednostki ktore maja swoje zadanie toolsy i moge sobie wykonywac to zadanie w srodku
node w langgraph odpowiada za pytanie, na tym etapie workflow kto ma sie wywolac
natomiast edge to po prostu miejsca gdzie jest polaczenie. 

czyli mozemy stworzyc 3 roznych agentow ktorzy beda mieli osobe zadania a mozemy je umiescic w jedym node, 
node to kamienie na rzece, na kamieniach moze byc mech, kamyczki i inne, a woda to nasze workflow, kamyczki sa polaczone edge tam gdzie sie styka mozna przejsc a tam gdzie nie to nie mozna

