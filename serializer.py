import base64
import os

class Serializer:
    def _bytes_to_string(self, data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')

    def _string_to_bytes(self, data: str) -> bytes:
        return base64.b64decode(data.encode('utf-8'))

    def save(self, data: bytes, filename: str):
        string = "Don`t change this file manually!!!!" + self._bytes_to_string(data)
        
        with open(filename, 'wt') as file:
            file.write(string)

    def load(self, filename: str) -> bytes:
        b = bytes()
        string = str()
        try:
            with open(filename, 'rt') as file:
                string = file.read()[len("Don`t change this file manually!!!!"):]
                b = self._string_to_bytes(string)
                if len(b) == 0:
                    raise Exception()
                
            with open(filename + 'copy', 'wt') as file: # Backup.
                    file.write("Don`t change this file manually!!!!" + string)
        except Exception:
            print("Your database is corrupted! Loading a backup.")
            try:
                with open(filename + "copy", 'rt') as file:
                    string = file.read()[len("Don`t change this file manually!!!!"):]
                    b = self._string_to_bytes(string)
                    
                with open(filename, 'wt') as file: # Restore.
                    file.write("Don`t change this file manually!!!!" + string)
            except Exception:
                print("Your backup is corrupted!!!!!!!!!") # Bad( .
        return b
    
    def get_files_in_directory(self, directory: str, extension: str) -> list:
        files = []
        for file in os.listdir(directory):
            if file.endswith(extension):
                files.append(file[: len(file) - len(".passman")])
        return files