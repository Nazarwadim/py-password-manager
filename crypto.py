from user import UserData
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import hashlib
import json

class CryptoHasher:
    def hash(self, password : str) -> bytes:
        sha3_256 = hashlib.sha3_256()
        sha3_256.update(password.encode('utf-8'))
        return sha3_256.digest()
    
class Crypto:
    _crypto_hasher = CryptoHasher()
    
    def __init__(self, password : str) -> None:
        self._hash = self._crypto_hasher.hash(password)

    def encrypt_data(self, data : bytes):
        iv = os.urandom(16)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(self._hash), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return iv + encrypted_data

    def decrypt_data(self, encrypted_data : bytes) -> bytes:
        iv = encrypted_data[:16]
        actual_encrypted_data = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self._hash), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(actual_encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data

    def encrypt_user_data_list(self, user_data_list : list[UserData]) -> bytes:
        json_data = json.dumps([user_data.to_dict() for user_data in user_data_list]).encode('utf-8')
        encrypted_data = self.encrypt_data(json_data)
        return encrypted_data

    def decrypt_user_data_list(self, encrypted_data : bytes) -> list[UserData]:
        decrypted_json_data = self.decrypt_data(encrypted_data)
        data_list = json.loads(decrypted_json_data.decode('utf-8'))
        return [UserData.from_dict(data) for data in data_list]