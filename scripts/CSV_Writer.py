import xlwings as xw
from abc import ABC, abstractmethod
from Writer import Writer
# För att inte läsa av webhallen hela tiden
# r"C:\Users\Gustav\Desktop\företag\review_data.xlsx"
'''
Folder med CSV som har namn av kategorin
sen:


item separator
leftmost[0], data_lists[0][0], data_lists[0][1], ...
leftmost[1], data_lists[1][0], ...
.
.
.
item separator
'''


class CSV_Writer(Writer):
    def __init__(self, folder_location: str) -> None:
        self.folder_location = folder_location
        self.current_file = None
        self.current_row = 0

    def set_file(self, file_name: str) -> None:
        self.current_row = 0
        file_name = self._make_name_legal(file_name)
        self.current_file = self.open_file()

    def open_file(self, file_name):
        return open(self.folder_location + file_name, "w")
    

    
    def _make_name_legal(self, name: str) -> str:
        # turns name into legal csv name
        illegal_characters = r":\/=*[]"
        return name.translate({ord(symbol) : None for symbol in illegal_characters})[:31]    

    
    def write(self, leftmost_entries: list[str], data_lists: list[list[str]], link: str = "") -> None:
        '''
        leftmost_entries go to the far left (for example, title or other summarizing information)
        data_lists are of arbitrary length that extend to the right
        optionally add a link to to top left entry
        '''
        if self.file is None:
            print("Sheet not set")
            return
        
        # special case for adding link
        self.sheet[self.current_row, 0].add_hyperlink(link, leftmost_entries[0])
        for sub_row, leftmost_entry in enumerate(leftmost_entries[1:]):
            self.sheet[self.current_row+sub_row+1, 0].value = leftmost_entry

        for sub_row, data_list in enumerate(data_lists):
            self.sheet[self.current_row + sub_row, 1].value = data_list
        
        height = max(len(data_lists), len(leftmost_entries))
        width = max([len(data_list) for data_list in data_lists])+1
        self.draw_square(height, width)

        self.current_row += height

    
    def draw_square(self, height: int, width: int) -> None:
        # make pretty
        # väldigt ful ruta just nu
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(7).Weight=2
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(8).Weight=2
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(9).Weight=2
        self.sheet[self.current_row:(self.current_row+height), 0:width].api.Borders(10).Weight=2


    
    def close(self) -> None:
        self.book.save()
        self.app.quit()
    
    def save(self) -> None:
        self.book.save()


