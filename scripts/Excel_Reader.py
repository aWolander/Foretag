from collections import defaultdict
import xlwings as xw
import pandas as pd
from Reader import Reader, Super_Reader

class Sheet_Reader(Reader):
    def __init__(self, entry_size: int, sheet: xw.Sheet) -> None:
        super.__init__(entry_size, sheet)

    def __iter__(self):
        return self

    def __next__(self) -> pd.DataFrame:
        '''
        returns: [data_names, data_lists] 
        '''

        data_lists = []
        data_names = self.file[self.current_row:(self.current_row+self.entry_size), 0].value
        if data_names == [None]*self.entry_size:
            raise StopIteration
        
        # try:
        #     data_names.append(self.file[self.current_row, 0].hyperlink)
        # except:
        #     #  Exception("The cell doesn't seem to contain a hyperlink!")
        #     # nån annan får fixa
        #     data_names.append("")
        
        for sub_row in range(self.entry_size):
            current_column = 1
            temp_list = []
            while True:
                temp_cell_value = self.file[self.current_row+sub_row, current_column].value
                if temp_cell_value is None:
                    break
                temp_list.append(temp_cell_value)
                current_column += 1
            data_lists.append(temp_list)

        self.current_row += self.entry_size
        # entry_df = pd.DataFrame
        # d = {"leftmost": leftmost, "data_lists": data_lists}
        


        # return entry_df(data=d, dtype=str)
        return [data_names, data_lists]
    
    def get_df(self):
        return self.df

    def make_df(self) -> pd.DataFrame:
        '''
        makes a pandas dataframe of the whole sheet
        '''
        if self.df is None:
            # d = {leftmost_names: [], data_list_names: []}
            d = defaultdict(list)
            for [data_names, data_lists] in self:
                for i in range(len(data_names)):
                    d[data_names[i]].append(data_lists[i])
            self.df = pd.DataFrame(data=d)
        return self.df

    def get_name(self) -> str:
        return self.file.name
    

class Book_Reader(Super_Reader):
    def __init__(self, entry_size: int, location: str) -> None:
        # try:
        #     self.app = xw.apps[xw.apps.keys()[0]]

        # except:
        #     print("hej")
        super.__init__(entry_size, location)
        self.app = xw.App(visible=True, add_book=False)
        self.book = self.app.books.open(location, read_only=True)
        
        self.df = None

    def _generate_sub_readers(self):
        
        temp_sub_readers = []
        for sheet in self.book.sheets:
            temp_sub_readers.append(Sheet_Reader(self.entry_size, sheet))
        return temp_sub_readers

    def __iter__(self):
        return iter(self.sub_readers)
    
    def __next__(self) -> Sheet_Reader:
        return next(self.sub_readers)
    
    # def make_df(self,  leftmost_names: list[str], data_list_names: list[str]) -> None:
    #     for sheet in self.sheets:
    #         self.df.add({self.sheet.get_name(): sheet.make_df(leftmost_names, data_list_names)})



    