import pandas as pd
import Excel_Reader
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

'''
Okej så pandas gillar inte att ha dataframes med listor i sig när man ska plotta saker. För barplots till exempel räknar jag manuellt ut average nu osv, fult
Annan lösning är omformatera dataframen så att två rader efter varandra kan va samma produkt, exempel:
Title, User Rating, AI Rating
ACER PREDATOR, 4, 3
ACER PREDATOR, 5, 4
ACER PREDATOR, 2, 2
HP OMEN, 3, 4
HP OMEN, 4, 4
osv
Beroende på vad för plots vi vill ha kan detta bli nödvändigt i princip
Dessutom, om det är många produkter som inte har ratings, behöver dessa nog filtreras och omformateras med
'''

class Statistic_Analyzer:
    def __init__(self, file_path: str, entry_size: int):
        self.data_book = Excel_Reader.Book_Reader(entry_size, file_path)
        self.entry_size = entry_size


    def process_book(self):
        for sheet in self.data_book:
            self.visualize_sheet(sheet)

    def bar_plot(self,df,x,y,title,xlabel,ylabel):
        plt.figure(figsize=(8, 6))
        sns.barplot(x=x, y=y, data=df, color='b')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=90,fontsize=10)
        plt.show()

    def box_plot(self,df,x,y,title,xlabel,ylabel):
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df[[x, y]])
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()

    def word_cloud(self,df,title,df_label):
        wordcloud_text = ' '.join([' '.join(words) for words in df[df_label]])
        wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(wordcloud_text)
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title)
        plt.axis('off')
        plt.show()

    def visualize_sheet(self, sheet):
        # Set up the visualizations
        sheet.make_df(["Title", "Summary"], ["Reviews", "User Ratings", "Reviews Summaries", "AI Ratings", "Dates"])
        df = sheet.get_df()
        title_prefix = sheet.get_name()
        df['Average AI Rating'] = df['AI Ratings'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)  
        df['Average User Rating'] = df['User Ratings'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)
        self.bar_plot(df,'Title','Average User Rating',f'{title_prefix} - Average User Ratings per Product','Product','User Rating')
        self.bar_plot(df,'Title','Average AI Rating',f'{title_prefix} - Average AI Ratings per Product','Product','AI Rating') 
        self.box_plot(df,'Average AI Rating','Average User Rating',f'{title_prefix} - Rating Distribution','Source','Rating')
        self.word_cloud(df,f'{title_prefix} - Word Cloud for Products','Reviews Summaries')
