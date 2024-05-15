from user import UserData
from serializer import Serializer
from crypto import Crypto
import os

class DataBase:
    _data = list[UserData]
    _crypto = Crypto(" ")
    _is_open : bool = False
    _filename : str

    def __init__(self, serializer : Serializer) -> None:
        self._serializer = serializer
    
    def new(self, password : str, filename : str) -> None:
        self._filename = filename
        self._crypto = Crypto(password)
        b = self._crypto.encrypt_user_data_list([])
        self._serializer.save(b, filename + ".passman")
        self._data = []
        self._is_open = True
        
    def open(self, password : str, filename : str) -> None:
        self._filename = filename
        self._crypto = Crypto(password)
        b = self._serializer.load(filename + ".passman")
        self._data = self._crypto.decrypt_user_data_list(b)
        self._is_open = True
    
    def close(self) -> None:
        if(self._is_open == False):
            return
        b = self._crypto.encrypt_user_data_list(self._data)      
        self._serializer.save(b, self._filename + ".passman")
        self._crypto = Crypto(" ")
        self._data = []
        self._is_open = False
    
    def add_user_data(self, user_data : UserData) -> None:
        self._data.append(user_data)
    
    def remove_user_data(self, index : int) -> None:
        self._data.pop(index)

    def get_available_db_names(self) -> list[str]:
        current_directory = os.getcwd()
        return self._serializer.get_files_in_directory(current_directory, extension=".passman")
    
    def get_user_data_count(self) -> int:
        return len(self._data)
    
    def get_data(self) -> tuple[UserData]:
        return tuple(self._data)
    
    def get_user_data(self, index : int) -> UserData:
        return self._data[index]

    def is_open(self) -> bool:
        return self._is_open