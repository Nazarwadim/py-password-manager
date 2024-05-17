from user import UserData
from serializer import Serializer
from crypto import Crypto
import os

class DataBase:
    """
    The DataBase class represents a database for storing UserData objects.
    It provides methods for creating, opening, closing, and manipulating the data in the database.
    
    Attributes:
        _data (list[UserData]): List of user data.
        _crypto (Crypto): Object for encrypting/decrypting data.
        _is_open (bool): Status of the database being open.
        _filename (str): Filename for storing the database.
        _serializer (Serializer): Object for serializing/deserializing data.
    
    Methods:
        __init__(self, serializer: Serializer) -> None:
            Initializes the DataBase instance with the given serializer.
        
        new(self, password: str, filename: str) -> None:
            Creates a new database with a password and saves it to a file.
        
        open(self, password: str, filename: str) -> None:
            Opens an existing database with a password from the specified file.
        
        close(self) -> None:
            Closes the database, saving it to a file.
        
        add_user_data(self, user_data: UserData) -> None:
            Adds a new UserData object to the database.
        
        remove_user_data(self, index: int) -> None:
            Removes a UserData object from the database by index.
        
        get_available_db_names(self) -> list[str]:
            Returns a list of database filenames available in the current directory.
        
        get_user_data_count(self) -> int:
            Returns the number of UserData objects in the database.
        
        get_data(self) -> tuple[UserData]:
            Returns all UserData objects in the database as a tuple.
        
        get_user_data(self, index: int) -> UserData:
            Returns the UserData object at the specified index.
        
        is_open(self) -> bool:
            Returns the status of the database being open.
    """
    _data = list[UserData]
    _crypto = Crypto(" ")
    _is_open : bool = False
    _filename : str

    def __init__(self, serializer : Serializer = Serializer()) -> None:
        """
        Initializes the DataBase instance with the given serializer.
        
        Args:
            serializer (Serializer): Object for serializing/deserializing data.
        """
        self._serializer = serializer
    
    def new(self, password : str, filename : str) -> None:
        """
        Creates a new database with a password and saves it to a file.
        
        Args:
            password (str): Password for encrypting the database.
            filename (str): Filename for storing the database.
        """
        self._filename = filename
        self._crypto = Crypto(password)
        b = self._crypto.encrypt_user_data_list([])
        self._serializer.save(b, filename + ".passman")
        self._data = []
        self._is_open = True
        
    def open(self, password : str, filename : str) -> None:
        """
        Opens an existing database with a password from the specified file.
        
        Args:
            password (str): Password for decrypting the database.
            filename (str): Filename from which to load the database.
        """
        self._filename = filename
        self._crypto = Crypto(password)
        b = self._serializer.load(filename + ".passman")
        self._data = self._crypto.decrypt_user_data_list(b)
        self._is_open = True
    
    def close(self) -> None:
        """
        Closes the database, saving it to a file.
        """
        if(self._is_open == False):
            return
        b = self._crypto.encrypt_user_data_list(self._data)      
        self._serializer.save(b, self._filename + ".passman")
        self._crypto = Crypto(" ")
        self._data = []
        self._is_open = False
    
    def add_user_data(self, user_data : UserData) -> None:
        """
        Adds a new UserData object to the database.
        
        Args:
            user_data (UserData): The user data to add.
        """
        self._data.append(user_data)
        b = self._crypto.encrypt_user_data_list(self._data)      
        self._serializer.save(b, self._filename + ".passman")
    
    def remove_user_data(self, index : int) -> None:
        """
        Removes a UserData object from the database by index.
        
        Args:
            index (int): The index of the user data to remove.
        """
        self._data.pop(index)

    def get_available_db_names(self) -> list[str]:
        """
        Returns a list of database filenames available in the current directory.
        
        Returns:
            list[str]: List of filenames with the .passman extension.
        """
        current_directory = os.getcwd()
        return self._serializer.get_files_in_directory(current_directory, extension=".passman")
    
    def get_user_data_count(self) -> int:
        """
        Returns the number of UserData objects in the database.
        
        Returns:
            int: The count of UserData objects.
        """
        return len(self._data)
    
    def get_data(self) -> tuple[UserData]:
        """
        Returns all UserData objects in the database as a tuple.
        
        Returns:
            tuple[UserData]: Tuple of all user data in the database.
        """
        return tuple(self._data)
    
    def get_user_data(self, index : int) -> UserData:
        """
        Returns the UserData object at the specified index.
        
        Args:
            index (int): The index of the user data to return.
        
        Returns:
            UserData: The user data at the specified index.
        """
        return self._data[index]

    def is_open(self) -> bool:
        """
        Returns the status of the database being open.
        
        Returns:
            bool: True if the database is open, False otherwise.
        """
        return self._is_open