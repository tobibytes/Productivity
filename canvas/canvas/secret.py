from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

class KeyEncryptor:
    _key_path = '../key.txt'

    if os.path.exists(_key_path):
        with open(_key_path, 'rb') as f:
            encoded_key = f.read()
            _key = base64.b64decode(encoded_key)
    else:
        _key = AESGCM.generate_key(bit_length=256)
        with open(_key_path, 'wb') as f:
            f.write(base64.b64encode(_key))

    _aesgcm = AESGCM(_key)

    @staticmethod
    def encrypt(plaintext: str) -> str:
        nonce = os.urandom(12)
        ciphertext = KeyEncryptor._aesgcm.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode()

    @staticmethod
    def decrypt(encrypted_b64: str) -> str:
        raw = base64.b64decode(encrypted_b64)
        nonce, ciphertext = raw[:12], raw[12:]
        plaintext = KeyEncryptor._aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()



