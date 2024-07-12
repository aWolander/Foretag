import xlwings as xw

class Sheet_Reader:
    def __init__(self, entry_size: int, sheet: xw.Sheet) -> None:
        self.sheet = sheet
        self.current_row = 0
        self.entry_size = entry_size

    def __iter__(self):
        return self

    def __next__(self) -> list[list[str], list[str]]:
        '''
        return: [[text in leftmost column + link of first item at the end], [entries to the right]]
        '''
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
    

    def get_name(self) -> str:
        return self.sheet.name
    

class Book_Reader:
    def __init__(self, entry_size: int, location: str) -> None:
        # try:
        #     self.app = xw.apps[xw.apps.keys()[0]]

        # except:
        #     print("hej")
        self.app = xw.App(visible=True, add_book=False)
        self.book = self.app.books.open(location, read_only=True)
        self.sheet_readers = []
        for sheet in self.book.sheets:
            self.sheet_readers.append(Sheet_Reader(entry_size, sheet))

    def set_sheet(self, sheetname: str) -> None:
        try:
            self.book.sheets[sheetname].activate()
        except:
            print("Sheet does not exist")

    def __iter__(self):
        return iter(self.sheet_readers)
    
    def __next__(self) -> Sheet_Reader:
        return next(self.sheet_readers)
    
    