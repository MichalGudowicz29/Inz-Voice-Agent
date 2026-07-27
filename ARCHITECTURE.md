# Backlog projektu asystenta glosowego 

# pytania do rozwiazania
1. Czy tekst ktory wchodzi z transkrybcji powinien zostac przepuszczony przez jakis lifting przed wrzuceniem do modelu jezeli tak to jaki 


# glowne zalozenia 

# 0. Architektura
## Subagent architecture

| -> Router (agent ktory ocenia czy trzeba zawolac orkiestratora czy po prostu konwersacja) 
A. 
1. -> Planer (Plan, jakie narzedzia uzyc, jakie sa cele) 
2. -> Weryfikator (Sprawdza czy plan jest wykonalny, czy mamy odpowiednie narzedzia.) 
3. -> Orkiestrator ( Dostaje pelne informacje na temat co trzeba zrobic gotowy plan, wywoluje odpowiednich agentow, toolsy)
Pod orkiestratorem beda agenci odpowiedzialni za konkretne obszary, np. Calendar Agent, CLI Agent, Weather agent. 
4. -> Weryfikator ( Sprawdza czy plan jest wykonany zgodnie z 1. Planem, 2. Intencja uzytkownika ) 
5. -> output

B. 
1. -> Konwersacja 
2. -> output

### System prompty
##### Router (Few-shot) 
1. Router powinien przyjmowac prompt uzytkownika i oceniac czy wymaga dalszego dzialania.
A. Wymaga dalszego dzialania - wywolanie Plannera
B. Wymaga jedynie konwersacji - wywoluje Konwersatora 
Skad wiedziec czy zadanie jest zadaniem? Router musi byc bardzo swiadomy swoich narzedzi.

##### Planner
1. Planner przyjmuje prompt uzytkownika i rozbija go na czynniki pierwsze, na podstawie listy dostepnych narzedzi oraz agentow w pierwszej kolejnosci jako mus, musi okreslic wykonalnosc zadania bez obiecywania niemozliwego   
##### Weryfikator
1. Glownym zadaniem weryfikatora jest sprawdzenie czy plan opracowany przez Plannera ma szanse powodzenia, czy dobrze zaplanowal uzycie narzedzi, oraz czy struktura ktora zaproponowal jest optymalna.
2. Weryfikator to krytyk i najwieksza maruda w strukturze, musi byc ogromnym realista
3. Gdy ma jakies uwagi, wraca do planera z konkretnymi poprawkami, lub sam je poprawia jezeli sa nieznaczne
##### Orkierstrator
1. Dostane na wejsciu gotowy plan, zweryfikowany. 
2. Powoluje agentow poprzez toolsy, aby wykonac konkretne czesci zadania 
##### Weryfikator koncowy
1. Weryfikuje to co zostalo zrobionie poprzez toolsy z oryginalnym planem, oraz ustrukturyzowuje to wszystko co zostalo wykonane
##### Konwersacja
1. Dostajemy rozmowe, zwracamy tekst, program przybiera postac chatbota. 
# 1. Agent przyjmuje prompty w formie glosowej 

Glos -> Text -> Prompt template (tutaj jakis gpt-5-nano na wygladzenie promptu *opcjonalnie jezeli poprawi jakos*) -> Invoke agenta -> Response -> TTS

1. Glos przychodzi i wchodzi przez funkcje listen ktora wywolana jest i zwraca poprzez 'yield' dzieki czemu caly czas przechwytuje glos i jest w stanie zwracac prompty do kolejki 
2. Text zwracany przez funkcje listen() sprwadzic czy wygladzenie surowego tekstu agentem pozwoli uzyskac dokladniejsze wyniki wzgledem niewygladzonego tekstu 
3. Prompt template, ktory przedstawi glownemu agentowi ze uzytkownik przekazal glosowo XYZ i musi rozplanowac wykonanie jezeli jest przedstawione zadanie lub odpowiedziec 

# 2. TBA
