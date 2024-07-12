from collections import defaultdict
import xlwings as xw
import pandas as pd
import csv as csv
from abc import ABC

# tex sheet för excel, mapp för csv
class Reader(ABC):
    def __init__(self, entry_size: int, file) -> None:
        self.current_row = 0
        self.file = file
        self.entry_size = entry_size
        self.df = None

    def __iter__(self): # vet inte type hint för iter objekt
        return self

    def __next__(self) -> list[list[str], list[str]]:
        '''
        return: [[text in leftmost column + link of first item at the end], [entries to the right]]
        '''
        pass
    
    def get_df(self) -> pd.DataFrame | None:
        return self.df

    def make_df(self, leftmost_names: list[str], data_list_names: list[str]) -> None:
        if self.df is None:
            # d = {leftmost_names: [], data_list_names: []}
            d = defaultdict(list)
            for [leftmost, data_lists] in self:
                for i in range(len(leftmost_names)):
                    d[leftmost_names[i]].append(leftmost[i])
                for i in range(len(data_list_names)):
                    d[data_list_names[i]].append(data_lists[i])
                
            self.df = pd.DataFrame(data=d)

    def get_name(self) -> str:
        return self.name

# tex book för excel, mapp för csv
class Super_Reader(ABC):
    def __init__(self, entry_size: int, location: str) -> None:
        self.sub_readers = self._generate_sub_readers()
        self.df = None

    def _generate_sub_readers(self) -> list:
        '''
        kanske inte funkar, kanske inte värt besväret
        '''
        pass

    def __iter__(self):
        pass
    
    def __next__(self):
        pass
    
    def make_df(self,  leftmost_names: list[str], data_list_names: list[str]) -> None:
        for sub_reader in self.sub_readers:
            self.df.add({self.sheet.get_name(): sub_reader.make_df(leftmost_names, data_list_names)})
