import xlwings as xw


class Book_Reader:
    def __init__(self, entry_size: int, location: str):
        # try:
        #     self.app = xw.apps[xw.apps.keys()[0]]

        # except:
        #     print("hej")
        self.app = xw.App(visible=True, add_book=False)
        self.book = self.app.books.open(location, read_only=True)
        self.sheet_readers = []
        for sheet in self.book.sheets:
            self.sheet_readers.append(Sheet_Reader(entry_size, sheet))

    def set_sheet(self, sheetname):
        try:
            self.book.sheets[sheetname].activate()
        except:
            print("Sheet does not exist")

    def __iter__(self):
        return iter(self.sheet_readers)
    
    def __next__(self):
        return next(self.sheet_readers)
    
    
class Sheet_Reader:
    def __init__(self, entry_size: int, sheet: xw.Sheet):
        self.sheet = sheet
        self.current_row = 0
        self.entry_size = entry_size

    def __iter__(self):
        return self

    def __next__(self) \
        -> list[list[str], list[str]]:
        # [[text in leftmost column + link of first item at the end], [entries to the right]]
        
        data_lists = []
        leftmost_entries = self.sheet[self.current_row:(self.current_row+self.entry_size), 0].value
        if leftmost_entries == []:
            raise StopIteration
        leftmost_entries.append(self.sheet[self.current_row, 0].hyperlink)
        
        for sub_row in range(self.entry_size):
            current_column = 1
            temp_list = []
            while True:
                temp_cell_value = self.sheet[self.current_row+sub_row, current_column].value
                if temp_cell_value is None:
                    break
                temp_list.append(temp_cell_value)
                current_column += 1
            data_lists.append(temp_list)

        self.current_row += self.entry_size

        return [leftmost_entries, data_lists]
    

    def get_name(self) \
        -> str:
        return self.sheet.name
    
    # def get_entry_name(self) \
    #     -> str:
    #     return self.sheet[self.current_row, 0].value


    

    # def read_all_products_from_excel(self):
    #     while True:
    #         product_name = data_sheet[current_row, 0].value
    #         if product_name is None:
    #             break
    #         temp_reviews = read_one_product_from_excel(current_row)
    #         current_row += 2


    # while True:
    #         if data_sheet[current_row, 0].value is None:
    #             break
    #         current_column = 1
    #         # ai.give_product_name(data_sheet[current_row,0].value)
    #         write_sheet[current_row,0].value = data_sheet[current_row,0].value
    #         while True:
    #             if data_sheet[current_row, current_column].value is None:
    #                 summary = ai.summary()
    #                 write_sheet[current_row+1, 0].value = summary
    #                 ai.clear_chat()
    #                 break
    #             rating = ai.interpret_review(data_sheet[current_row, current_column].value)
    #             write_sheet[current_row, current_column].value = rating
    #             write_sheet[current_row+1, current_column].value = data_sheet[current_row+1, current_column].value

    #             current_column += 1
    #         current_row += 2