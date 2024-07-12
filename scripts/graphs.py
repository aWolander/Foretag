import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def clean_data(df):
    products = []
    chatgpt_ratings = []
    user_ratings = []
    chatgpt_words = []

    for row in range(0, len(df), 3): #Dependent on excel format, at time of writing there was 3 rows per product. 
        # Extract product name
        product_name = df.iloc[row, 0]
        # Extract the corresponding ChatGPT words
        chatgpt_word = str(df.iloc[row+1, 0])
        # Extract ratings
        chatgpt_rating_row = df.iloc[row, 1:].dropna().tolist()
        user_rating_row = df.iloc[row + 1, 1:].dropna().tolist()

        
        if len(chatgpt_rating_row) == len(user_rating_row):
            products.extend([product_name] * len(chatgpt_rating_row))
            chatgpt_ratings.extend(chatgpt_rating_row)
            user_ratings.extend(user_rating_row)
            chatgpt_words.extend([chatgpt_word] * len(chatgpt_rating_row))
    
    chatgpt_words = [word.replace('Kvalitet', '') for word in chatgpt_words] #Remove the word 'Kvalitet' from the word cloud since it appears randomly

    cleaned_data = pd.DataFrame({
        'Product': products,
        'ChatGPT Rating': chatgpt_ratings,
        'User Rating': user_ratings,
        'ChatGPT Words': chatgpt_words
    })

    cleaned_data['Short Product'] = cleaned_data['Product'].apply(lambda x: ' '.join(x.split()[:3]))

    return cleaned_data

def create_visualizations(cleaned_data, title_prefix):
    # Set up the visualizations
    plt.figure(figsize=(18, 10))

    # Separate bar charts for average ratings, too many products in one plot otherwise
    plt.subplot(2, 3, 1)
    sns.barplot(x='Short Product', y='ChatGPT Rating', data=cleaned_data, color='b')
    plt.title(f'{title_prefix} - Average ChatGPT Ratings per Product')
    plt.ylabel('ChatGPT Rating')
    plt.xlabel('Product')
    plt.xticks(rotation=90)

    plt.subplot(2, 3, 2)
    sns.barplot(x='Short Product', y='User Rating', data=cleaned_data, color='r')
    plt.title(f'{title_prefix} - Average User Ratings per Product')
    plt.ylabel('User Rating')
    plt.xlabel('Product')
    plt.xticks(rotation=90)

    # Box plot of rating distributions
    plt.subplot(2, 3, 3)
    sns.boxplot(data=cleaned_data[['ChatGPT Rating', 'User Rating']])
    plt.title(f'{title_prefix} - Rating Distribution')
    plt.ylabel('Rating')
    plt.xlabel('Source')

    # Word cloud for review content - Generating a sample word cloud based on ChatGPT words 
    wordcloud_text = ' '.join(cleaned_data['ChatGPT Words'])
    wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(wordcloud_text)
    plt.subplot(2, 3, 6)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'{title_prefix} - Word Cloud for Products')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


file_path = 'd:/pythonProject1/Company/chatgpt_output2.xlsx'
data = pd.read_excel(file_path, sheet_name=['Kablar & Adapters', 'VR-Headset', 'Hemmakontoret', 'Stationär dator'], header=None)

# Process and visualize each sheet
for sheet_name, df in data.items():
    cleaned_data = clean_data(df)
    create_visualizations(cleaned_data, sheet_name)

