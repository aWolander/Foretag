# Foretag

Ni kommer behöva några libraries. ba googla vad som importerar å ni lär hitta det.

Skriv i snake_case, inte CamelCase eller något annat. Klasser är i Stora Bokstäver. Försök vara så explicit som möjligt i variabel/funktionsnamn. 
Jag vill inte se otydliga variabelnamn. Dödsstraff om ni döper variabler till typ "i" eller "temp". Skriv i princip aldrig:
```py
for i in range(list):
  do_something(i)
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

Använd type hints. Kommer göra allt lättare i längden. Det är hela 
```py
def blabla(number: int) -> str: 
    return "blablabla"
```
Det här specar att man sätter in en siffra och får ut en string. 
Om man kan få ut flera olika datatyper ur en funktion så borde ni nog skriva om funktionen.
Ni kommer kanske behöva uppdatera python för att inte få error här. Vissa type hints är python 3.9+.

Gör inte inheritence på mer än ett lager om ni inte verkligen, verkligen känner att det behövs.

Jag har försökt va konsekvent med sortens kommentarer

Om ni kan lista ut ett bra sätt att göra så att xlwings inte öppnar massor av jävla fönster hela fucking tiden när man kör programmet flera gånger så får ni puss på kinden.

Angående kommentarer, använd ''' ''' för längre kommentarer, i början av funktioner och/eller för att speca hur returns ser ut i mer komplicarade fall, till exempel:
```py
def scrape_category(self, category_name: str, category_id: str) -> None:
    '''
    scrapes AND writes to excel. dont like that.
    Want to seperate writing and scraping, but then I would have to write a whole category at a time.
    rip memory.
    '''
```
Använd # för korta kommentarer i funktioner, till exempel:
```py
if reviews_html == []:
    # When product has no reviews. will return [[],"",[]]
    return [reviews_text, review_dates, total_stars, review_stars]
```
Unvik att ha för många

