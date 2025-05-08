from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

class KeyEncryptor:
    _key = AESGCM.generate_key(bit_length=256)
    _aesgcm = AESGCM(_key)

    @staticmethod
    def encrypt(plaintext: str) -> str:
        """
        Encrypts the given string and returns a base64-encoded ciphertext.
        """
        nonce = os.urandom(12)
        ciphertext = KeyEncryptor._aesgcm.encrypt(nonce, plaintext.encode(), None)
        encrypted = base64.b64encode(nonce + ciphertext).decode()
        return encrypted

    @staticmethod
    def decrypt(encrypted_b64: str) -> str:
        """
        Decrypts a base64-encoded string and returns the original plaintext.
        """
        raw = base64.b64decode(encrypted_b64)
        nonce, ciphertext = raw[:12], raw[12:]
        plaintext = KeyEncryptor._aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()