import openai
openai.api_key = "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"
# Ska den läsa föregående reviews?
# Temperature?
# n?
# max_tokens?
# exempel på rätt format

'''
TODO:
Ha någon verify_output(ai_output) och be ain försöka igen tills den får rätt format. 
Billigare att iterera över flera alternativ (n>1) för vissa funktioner så input-meddelandena inte
itereras flera gånger.
Bättre promts, alltid.
'''
class Review_assistant:
    def __init__(self) -> None:
        self.messages = []
        self.texts = []
        self.initial_rating_messages = [{"role": "system", "content":
            "Du är en hjälpsam assisten som kommer tolka recensioner från användare på en produkt och svara på en skala 1-5 hur positiv"
            "recensionen är. Du ska endast skriva en siffra som svar, inget annat."}]
        self.summary_messages = [{"role": "system", "content":"Vad tyckte användarna var viktigast?" 
            "Belys upp till tre exempel. Använd endast ett nyckelord. Ha alla recensioner i åtanke."}]
        self.initial_sentiment_messages = [{"role": "system", "content": 
            "Du är en hjälpsam assistent som kommer avgöra vad användare tyckte var viktigast"
            "i en recension på en produkt eller tjänst. Ha endast en recension i åtanke i taget. Bry dig inte om det folk har sagt tidigare."
            "Belys upp till tre exempel. Använd endast ett nyckelord. Du får endast ge tre nyckelord som svar, utveckla inte vidare." 
            "Ha med både det användaren"
            "tyckte var negativt och positivt."},
            {"role": "user", "content":"Är nöjd med denna, riktigt snabb. Men den är tyvärr rättså tung."},
            {"role":"assistant", "content":"Prestanda, Tyngd"},
            {"role":"user", "content":"Mycket dator för pengarna och relativt tyst. Har funkat utmärkt än så länge, rekommenderas!"},
            {"role":"assistant", "content":"Pris, Ljudnivå"}]
        # self.single_reviews_message= {"role": "system", "content":
        #     "Du är en hjälpsam assisten som kommer bli given recensioner på en produkt skrivna av olika användare."
        #     "Du ska avgöra vad användarna ansåg var viktigast med produkten." 
        #     "Belys upp till tre exempel. Använd endast ett nyckelord. Ha alla recensioner i åtanke."}
    
    # def analyze_texts(self, initial_message, )

    def rate_reviews(self) -> list[str]:
        temp_messages = self.initial_rating_messages
        ratings = []
        for review_message in self.messages:
            temp_messages.append(review_message)
            chat = openai.chat.completions.create(
                model="gpt-3.5-turbo", 
                temperature=0.2, 
                messages=temp_messages,
                n=3,
                max_tokens=1
            )
            rating = chat.choices[0].message.content
            temp_messages.append(self._string_to_message_format("assistant", rating))
            ratings.append(rating)
        return ratings
    
    def summarize(self) -> list[str]:
        temp_messages = self.summary_messages + self.messages
        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo", 
            temperature=0.2, 
            messages=temp_messages,
            n = 1,
            max_tokens = 20
        )
        summary = chat.choices[0].message.content
        return summary

    def sentiment_reviews(self) -> list[str]:
        temp_messages = self.initial_sentiment_messages + self.messages
        sentiments = []
        for message in self.messages:
            temp_messages.append(message)
            chat = openai.chat.completions.create(
                model="gpt-3.5-turbo", 
                temperature=0.2, 
                messages=temp_messages,
                n=1,
                max_tokens=20
            )
            sentiment = chat.choices[0].message.content
            temp_messages.append(self._string_to_message_format("assistant", sentiment))
            sentiments.append(sentiment)
        return sentiments
    
    def add_texts(self, texts: list[str]) -> None:
        self.texts += texts
        self.messages += self._strings_to_message_format("user", texts)

    def _string_to_message_format(self, role: str, text: str) -> dict[str, str]:
        return {"role": role, "content":text}

    def _strings_to_message_format(self, role: str, texts: list[str]) -> list[dict[str, str]]:
        return [self._string_to_message_format(role, text) for text in texts]

    
    def clear_chat(self) -> None:
        self.messages = []
        self.texts = []
    
    
    def give_product_name(self, name: str) -> None:
        # Depreceated
        self.rating_messages.append({"role": "system", "content":"Produktens namn är: " + name})

    
       # def interpret_review_single(self, review):
    #     self.reviews.append(review)
    #     temp_messages = self.rating_messages
    #     self.rating_messages.append(
    #         {"role": "user", "content":review})
    #     chat = openai.chat.completions.create(
    #         model="gpt-3.5-turbo", 
    #         temperature=0.2, 
    #         messages=temp_messages,
    #         n=3,
    #         max_tokens=1
    #     )
    #     rating = chat.choices[0].message.content
    #     return rating
    
    # def get_review(self, message):
    #     self.review_interpreter.append({"role": "user", "content": message})

    # def update_system(self, message):
    #     self.review_interpreter.append({"role": "system", "content": message})

    # def summarize_single(self):
    #     input_messages = [self.single_reviews_message, 
    #                       {"role": "user", "content":self.reviews.join("\n")}
    #                       ]
    

# "Till exempel:"
#              "Vi har följande recensioner: "
#              "\"Hårdvaran är bra byggd som vanligt med apple, "
#              "trevligt med hdmi m.m så man inte måste hålla på med adapter hela tiden. "
#              "Bra prestanda och riktigt nöjd med batteritiden, "
#              "håller en arbetsdag och ibland 2 vid lättare arbeten.\","
#              "\"Längre batteritid går aldrig fel.\","
#              "\"Bra prestanda och bra batteritid, toppen!\""
#              "Du ska då svara: \"Batteritid, prestanda\""

# Till exmpel:" 
#             "Recension: \"Bytte upp mig från en MacBook Pro 2017. Helt klart värt det. Tangentbord, skärm, finish och trackpad är världsklass.\""
#             "Svar: \"5\
