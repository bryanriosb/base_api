import os
import json
import base64
import numpy as np

from cryptography.fernet import Fernet

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class ProtectData:
    """Allow cypher and decode bytes with cryptography."""

    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        # We create a Fernet object using the secret key.
        password = os.getenv("ENCRYPT_KEY")
        self.fernet_cipher = Fernet(password)
        # AES Cipher
        # AES_KEY 128 bits key with base64 encoding.
        aes_key = base64.b64decode(os.getenv("AES_KEY"))
        aes_iv = base64.b64decode(os.getenv("AES_IV"))
        self.aes_cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    def encode_to_bytes(self):
        bytes_data = None
        # If this is a string
        if isinstance(self.data, str):
            bytes_data = self.data.encode()
        # If this is a json, become to JSON string
        elif isinstance(self.data, dict):
            bytes_data = json.dumps(self.data).encode()
        return bytes_data

    @staticmethod
    def decode_uint8_array(arr_uint8):
        arr_decode = np.array(arr_uint8, dtype=np.uint8).tobytes().decode("ascii")
        return arr_decode

    def fernet_encrypt(self):
        """Symmetric key encryption like the one shown in the example above
         is very secure, but requires both parties to have the same
         key in order to encrypt and decrypt data."""
        # Parse to bytes
        bytes_data = self.encode_to_bytes()
        # Byte Data Encrypt
        encrypted_data = self.fernet_cipher.encrypt(bytes_data)
        # Create uint8 buffer to store in BinaryField
        arr_uint8 = np.frombuffer(encrypted_data, dtype=np.uint8)
        return arr_uint8

    def fernet_decrypt(self):
        try:
            # Parse memory object from BinaryField to uint8 buffer
            arr_uint8 = np.frombuffer(self.data, dtype=np.uint8)
            # Parse uint8 buffer to bytes
            decrypt_to_bytes = self.decode_uint8_array(arr_uint8)
            # Data Decrypt with bytes data
            data = self.fernet_cipher.decrypt(decrypt_to_bytes).decode()
            return data
        except Exception as e:
            print('Error decrypt', e)
            raise Exception("Can't decrypt data")

    def aes_encrypt(self):
        """Encrypt AES 128 bits."""
        bytes_data = self.encode_to_bytes()
        encrypted = self.aes_cipher.encrypt(pad(bytes_data, AES.block_size))
        b64_encrypted = base64.b64encode(encrypted).decode()
        return b64_encrypted

    def aes_decrypt(self):
        """Decrypt AES 128 bits."""
        byte_token = base64.b64decode(self.data)
        decrypted = unpad(self.aes_cipher.decrypt(byte_token), AES.block_size)
        return decrypted.decode()
