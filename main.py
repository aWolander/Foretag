        # self.write_book = xw.Book(r"C:\Users\Gustav\Desktop\företag\chatgpt_output.xlsx")
        # self.data_book = xw.Book(r"C:\Users\Gustav\Desktop\företag\review_data.xlsx")
import xlwings as xw
import Excel_Reader as xle
import Excel_Writer as xlw
from chatgpt_interface import Review_assistant
'''
TODO
behöver typ strippa alla textfält i review_data2... Jobbigt
app.kill() funkar fan inte bra. https://stackoverflow.com/questions/60906795/xlwings-cant-get-excel-application-to-quit-even-with-kill-method
'''

def main():
    print(xw.apps)
    for app in xw.apps:
        app.kill()
    print(xw.apps)
    reader = xle.Book_Reader(3, r"review_data2.xlsx")
    writer = xlw.Excel_Writer(r"chatgpt_output69.xlsx")
    ai = Review_assistant()
    for review_sheet in reader:
        print(review_sheet.get_name())
        writer.set_sheet(review_sheet.get_name())
        for [leftmost_entries, data_lists] in review_sheet:
            product_name = leftmost_entries[0]
            product_link = leftmost_entries[-1]
            reviews = data_lists[0]
            user_ratings = data_lists[1]
            dates = data_lists[2]

            # print(product_name)

            ai.add_texts(reviews)
            ai_ratings = ai.rate_reviews()
            ai_sentiments = ai.sentiment_reviews()
            ai_summary = ai.summarize()
            ai.clear_chat()
            writer.write([product_name, ai_summary], [reviews, user_ratings, ai_sentiments, ai_ratings, dates], link = product_link)

main()