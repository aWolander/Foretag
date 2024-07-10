import xlwings as xw
from abc import ABC, abstractmethod
# För att inte läsa av webhallen hela tiden
# r"C:\Users\Gustav\Desktop\företag\review_data.xlsx"

class Excel_Writer:
    def __init__(self, location: str) \
        -> None:
        # try:
        #     self.app = xw.apps[xw.apps.keys()[1]]
        # except:
        #     print("hej")
        #     self.app = xw.App(visible=True, add_book=False)
        
        self.app = xw.App(visible=True, add_book=False)
        try:
            self.book = self.app.books[location]
        except:
            self.book = self.app.books.add()
            self.book.save(location)
        self.sheet = None
        self.current_row = 0

    def set_sheet(self, sheet_name: str) \
        -> None:
        self.current_row = 0
        sheet_name = self._make_name_legal(sheet_name)
        try:
            self.book.sheets[sheet_name].activate()
        except: # Vad heter errorn? vem vet
            self.book.sheets.add(sheet_name) 
        self.sheet = self.book.sheets.active
        self.sheet.clear()


    
    def _make_name_legal(self, name: str) \
        -> None:
        # turns name into legal excel name
        illegal_characters = r":\/=*[]"
        return name.translate({ord(symbol) : None for symbol in illegal_characters})[:31]    

    
    def write(self, leftmost_entries: list[str], data_lists: list[list[str]], link: str = "") \
        -> None:
        if self.sheet is None:
            print("Sheet not set")
            return
        
        # special case for adding hyperlink
        self.sheet[self.current_row, 0].add_hyperlink(link, leftmost_entries[0])
        for sub_row, leftmost_entry in enumerate(leftmost_entries[1:]):
            self.sheet[self.current_row+sub_row+1, 0].value = leftmost_entry

        for sub_row, data_list in enumerate(data_lists):
            self.sheet[self.current_row + sub_row, 1].value = data_list
        
        height = max(len(data_lists), len(leftmost_entries))
        width = max([len(data_list) for data_list in data_lists])+1
        self.draw_square(height, width)

        self.current_row += height

    
    def draw_square(self, height: int, width: int) \
        -> None:
        # make pretty
        # väldigt ful ruta just nu
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(7).Weight=2
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(8).Weight=2
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(9).Weight=2
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(10).Weight=2


    
    def close(self) \
        -> None:
        self.book.save()
        self.app.quit()
    
    def save(self) \
        -> None:
        self.book.save()


