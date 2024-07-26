import pandas as pd
import Excel_Reader
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
import scipy.stats as stats
import matplotlib
matplotlib.use('TkAgg')  
'''
TODO:
Notera att varje filnamn är baserat på min laptop så måste ändras på andra datorer, ska skriva om senare så det inte behövs ändras.
SKriv om koden så att allt delas upp i funktioner snyggt å använd klassobjekt för allt. Fult å klumpigt som det är skrivet just nu.
Lägg till dokumentation å beskrivning av allt så det blir snyggare
Lägg till fler visualiseringar/grafer som johan kan använda sig av
Skriv om fula list comprehensions å for loopar
'''

class Statistic_Analyzer:
    def __init__(self, file_path: str, entry_size: int):
        self.data_book = Excel_Reader.Book_Reader(entry_size, file_path)
        self.entry_size = entry_size
        self.df = None
        self.title_prefix = None
        
    def process_book(self):
        for sheet in self.data_book:
            self.visualize_sheet(sheet)

    def bar_plot(self,df,x,y,title,xlabel,ylabel):
        file_name = f"C:\Python_programs\Company\Foretag\data_files\Images\{self.title_prefix}_bar_plot.png"
        plt.figure(figsize=(8, 6))
        sns.barplot(x=x, y=y, data=df, color='b')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=90,fontsize=10)
        plt.savefig(file_name)
      

    def box_plot(self,df,x,y,title,xlabel,ylabel):
        file_name = f"C:\Python_programs\Company\Foretag\data_files\Images\{self.title_prefix}_box_plot.png"
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df[[x, y]])
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.savefig(file_name)
        

    def word_cloud(self,df,title,df_label):
        file_name = r"C:\Python_programs\Company\Foretag\data_files\Images\\"
        wordcloud_text = ' '.join([' '.join(words) for words in df[df_label]])
        wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(wordcloud_text)
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title)
        plt.axis('off')
        plt.savefig(file_name+title +".png")
        plt.close()

    def normal_distribution(self,df):
        file_name = f"C:\Python_programs\Company\Foretag\data_files\Images\{self.title_prefix}_normal_distribution.png"
        all_ratings = [rating for sublist in df['AI Ratings'] for rating in sublist]
        mean = np.mean(all_ratings)
        std_dev = np.std(all_ratings)
        x = np.linspace(min(all_ratings), max(all_ratings), 100)
        y = stats.norm.pdf(x, mean, std_dev)
        plt.figure(figsize=(10, 6))
        plt.hist(all_ratings, bins=10, density=True, alpha=0.6, color='g', edgecolor='black')
        plt.plot(x, y, 'k', linewidth=2)
        plt.title(f"{self.title_prefix} - Normal Distribution of Ratings")
        plt.xlabel('Rating')
        plt.ylabel('Density')
        plt.savefig(file_name)
   
    def pad_lists(self,row):
        #Removes entries from User Ratings column such that it has same length as AI Ratings, if AI Ratings is longer this fails but should not happen
        length_difference = len(row['User Ratings'])-len(row['AI Ratings'])
        while length_difference > 0:
            row['User Ratings'].pop()
            length_difference -= 1
        return row

    def remove_strings(self,row):
        if any(isinstance(i, str) for i in row['User Ratings']):
            row['User Ratings'] = [None]
        if any(isinstance(i, str) for i in row['AI Ratings']):
            row['AI Ratings'] =[None] 
        return row
    

    def visualize_sheet(self, sheet):
        # Set up the visualizations
        sheet.make_df(["Title", "Summary"], ["Reviews", "User Ratings", "Reviews Summaries", "AI Ratings", "Dates"])
        self.df = sheet.get_df()
        self.title_prefix = sheet.get_name()
        
        #Remove empty lists from dataframe
        df_filtered = self.df.dropna()
        df_filtered = df_filtered[df_filtered['User Ratings'].map(len) > 0]
        df_filtered = df_filtered[df_filtered['AI Ratings'].map(len) > 0]

        #Make sure all rating lists are of same length
        df_filtered = df_filtered.apply(self.pad_lists, axis=1)
        
        #Remove strings from User Ratings and AI Ratings
        df_filtered = df_filtered.apply(self.remove_strings, axis=1)
        
        #Remove products with None in User Ratings or AI Ratings
        df_filtered = df_filtered[df_filtered['AI Ratings'].map(lambda x: None not in x)]
        df_filtered = df_filtered[df_filtered['User Ratings'].map(lambda x: None not in x)]
        
        #Calculate average ratings
        df_filtered['Average AI Rating'] = df_filtered['AI Ratings'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)  
        df_filtered['Average User Rating'] = df_filtered['User Ratings'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)
       
        #Filter positive and negative reviews
        df_filtered_exploded = df_filtered.explode('User Ratings')
        df_filtered_negative = df_filtered_exploded[df_filtered_exploded['User Ratings'] < 3]
        df_filtered_positive = df_filtered_exploded[df_filtered_exploded['User Ratings'] >= 3]

        #Plot everything
        self.bar_plot(df_filtered,'Title','Average User Rating',f'{self.title_prefix} - Average User Ratings per Product','Product','User Rating')
        self.bar_plot(df_filtered,'Title','Average AI Rating',f'{self.title_prefix} - Average AI Ratings per Product','Product','AI Rating') 
        self.box_plot(df_filtered,'Average AI Rating','Average User Rating',f'{self.title_prefix} - Rating Distribution','Source','Rating')
        if len(df_filtered['Reviews Summaries']) > 0 and len(df_filtered_negative['Reviews Summaries']) > 0 and len(df_filtered_positive['Reviews Summaries']) > 0:
            self.word_cloud(df_filtered,f'{self.title_prefix} - Word Cloud for Products','Reviews Summaries')
            self.word_cloud(df_filtered_negative,f'{self.title_prefix} - Word Cloud for Negative Products','Reviews Summaries')
            self.word_cloud(df_filtered_positive,f'{self.title_prefix} - Word Cloud for Positive Products','Reviews Summaries')
        self.normal_distribution(df_filtered,'User Ratings','AI Ratings')
        

        
        
