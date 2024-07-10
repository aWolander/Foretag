import xlwings as xw
from abc import ABC, abstractmethod
# För att inte läsa av webhallen hela tiden
# r"C:\Users\Gustav\Desktop\företag\review_data.xlsx"

class Scraping_writer:
    def __init__(self, location):
        self.app = xw.App(visible=True, add_book=False)
        self.book = self.app.books.open(location)
        self.data_sheet = None
        self.current_row = 0
        

    # @xw.func(async_mode='threading')
    def _set_sheet(self, sheet_name):
        self.current_row = 0
        sheet_name = self.make_name_legal(sheet_name)
        try:
            self.book.sheets[sheet_name].activate()
        except: # Vad heter errorn? vem vet
            self.book.sheets.add() 
            xw.books.active.sheets.active.name = str(sheet_name)
        self.data_sheet = self.book.sheets.active
        self.data_sheet.clear()
        
    def _write_data(self, product_url, product_name, reviews_text, reviews_dates, total_stars, review_stars):
        self.data_sheet[self.current_row, 0].add_hyperlink(product_url, product_name)
        self.data_sheet[self.current_row+1, 0].value = total_stars
        for i in range(len(reviews_text)):
            self.data_sheet[self.current_row, i+1].value = reviews_text[i]
            self.data_sheet[self.current_row+1, i+1].value = review_stars[i].split(" ")[0] # fuck you excel
            self.data_sheet[self.current_row+2, i+1].value = " " + str(reviews_dates[i])
        self.current_row += 3
    
    def write_data(self, product_url, product_name, reviews_text, reviews_dates, total_stars, review_stars):
        self._safe_exit(self._write_data, product_url, product_name, reviews_text, reviews_dates, total_stars, review_stars)

    def set_sheet(self, sheet_name):
        self._safe_exit(self._set_sheet, sheet_name)
        
        
    def _safe_exit(self, func, *args):
        try:
            func(*args)
        except KeyboardInterrupt:
            print(func)
            self.close()
    
    def make_name_legal(self, name):
        # turns name into legal excel name
        illegal_characters = r":\/=*[]"
        return name.translate({ord(symbol) : None for symbol in illegal_characters})[:31]
    
    def close(self):
        self.book.save()
        self.app.quit()
    
    def save(self):
        self.book.save()

class AI_writer:
    def __init__(self, location):
        self.app = xw.App(visible=True, add_book=False)
        self.book = self.app.books.open(location)
        self.app.visible = True
        self.sheet = None

        self.current_row = 0
    
    def write_next_product(self, product_name, summary, ai_ratings, user_ratings, dates):
        self.write_for_one_product(product_name, summary, ai_ratings, user_ratings, dates)
        self.current_row += 3
    
    def add_category(self, category_name):
        try:
            self.book.sheets(category_name).activate()
            self.sheet = self.book.sheets.active 
            self.sheet.clear()
        except:
            self.book.sheets.add(category_name)
            self.sheet = self.book.sheets.active
        self.current_row = 0

# Hyperlinks vore najs
    def write_for_one_product(self, product_name, summary, ai_ratings, user_ratings, dates):
        current_column = 1

        self.sheet[self.current_row, 0].value = product_name
        # self.sheet[self.current_row, 0].add_hyperlink(product_url, product_name)
        self.sheet[self.current_row+1, 0].value = summary
        for [ai_rating, user_rating, date] in zip(ai_ratings, user_ratings, dates):
            self.sheet[self.current_row, current_column].value = ai_rating
            self.sheet[self.current_row+1, current_column].value = user_rating
            self.sheet[self.current_row+2, current_column].value = date


            current_column += 1
        
    def close(self):
        self.book.save()
        self.app.quit()



