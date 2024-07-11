# Foretag

Ni kommer behöva några libraries. ba googla vad som importerar å ni lär hitta det.

Skriv i snake_case, inte CamelCase eller något annat. Klasser är i Stora Bokstäver. Försök vara så explicit som möjligt i variabel/funktionsnamn. 
Jag vill inte se otydliga variabelnamn. Dödsstraff om ni döper variabler till typ "i" eller "temp". Skriv i princip aldrig:
```
for i in range(list)
```
Det finns typ alltid ett bättre namn än "i".

Ofta i koden så skriver jag variabler i plural för att indikera en lista. T.ex test_reviews är en lista, test_review är ett objekt i den listan.

Var inte rädd för att göra många funktioner. Bättre det än långa.

Undvik att nesta mer än ett eller två lager. Ibland behövs det men försök att unvika något som ser ut som:
```
for:
  for:
    if:
      do_something()
    else:
      for:
        do_something_else()
````
Det är en mardröm att läsa.

Använd type hints. Kommer göra allt lättare i länden. Det är hela 
```
def blabla(number: int) -> str: 
return "blablabla"
```
Det här specar att man sätter in en siffra och får ut en string. 
Om man kan få ut flera olika datatyper ur en funktion så borde ni nog skriva om funktionen.
Ni kommer kanske behöva uppdatera python för att inte få error här. Vissa type hints är python 3.9+.

Gör inte inheritence på mer än ett lager om ni inte verkligen, verkligen känner att det behövs.

Om ni kan lista ut ett bra sätt att göra så att xlwings inte öppnar massor av jävla fönster hela fucking tiden när man kör programmet flera gånger så får ni puss på kinden.

