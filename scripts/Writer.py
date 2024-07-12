import xlwings as xw
from abc import ABC, abstractmethod
# För att inte läsa av webhallen hela tiden
# r"C:\Users\Gustav\Desktop\företag\review_data.xlsx"

class Writer(ABC):
    def __init__(self, location: str) -> None:
        pass

    @abstractmethod
    def _make_name_legal(self, name: str) -> str:
        # turns name into legal excel name
        pass

    @abstractmethod
    def write(self, leftmost_entries: list[str], data_lists: list[list[str]], link: str = "") -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass


