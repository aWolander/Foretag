import xlwings as xl

book = xl.Book("review_data3.xlsx")
book.sheets[0][0,3].value = "'4 / 5"