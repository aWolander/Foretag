import pandas as pd
import Excel_Reader
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

class Statistic_Analyzer:
    def __init__(self, file_path: str, entry_size: int):
        self.data_book = Excel_Reader.Book_Reader(file_path, entry_size)
        self.entry_size = entry_size


    def process_book(self):
        for sheet in self.data_book:
            self.visualize_sheet(sheet)

    def visualize_sheet(self, sheet):
        # Set up the visualizations
        sheet.make_df(["Title","Summary"], ["Reviews", "User Stars"])
        df = sheet.get_df()
        plt.figure(figsize=(18, 10))

        # Separate bar charts for average ratings, too many products in one plot otherwise
        plt.subplot(2, 3, 1)
        sns.barplot(x='Short Product', y='ChatGPT Rating', data=df, color='b')
        plt.title(f'{title_prefix} - Average ChatGPT Ratings per Product')
        plt.ylabel('ChatGPT Rating')
        plt.xlabel('Product')
        plt.xticks(rotation=90)

        plt.subplot(2, 3, 2)
        sns.barplot(x='Short Product', y='User Rating', data=df, color='r')
        plt.title(f'{title_prefix} - Average User Ratings per Product')
        plt.ylabel('User Rating')
        plt.xlabel('Product')
        plt.xticks(rotation=90)

        # Box plot of rating distributions
        plt.subplot(2, 3, 3)
        sns.boxplot(data=df[['ChatGPT Rating', 'User Rating']])
        plt.title(f'{title_prefix} - Rating Distribution')
        plt.ylabel('Rating')
        plt.xlabel('Source')

        # Word cloud for review content - Generating a sample word cloud based on ChatGPT words 
        wordcloud_text = ' '.join(df['ChatGPT Words'])
        wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(wordcloud_text)
        plt.subplot(2, 3, 6)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'{title_prefix} - Word Cloud for Products')
        plt.axis('off')

        plt.tight_layout()
        plt.show()



