import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _load_key() -> bytes:
    """
    Load the AES-256-GCM key.

    Resolution order:
      1. CANVAS_ENCRYPTION_KEY env var (base64-encoded 32-byte key) — preferred.
      2. Local ./key.txt file (legacy; gitignored).
      3. Generate a fresh key and persist it to ./key.txt on first run.

    Never commit key.txt. In any deployed environment, set CANVAS_ENCRYPTION_KEY.
    """
    env_key = os.environ.get("CANVAS_ENCRYPTION_KEY")
    if env_key:
        return base64.b64decode(env_key)

    key_path = "./key.txt"
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return base64.b64decode(f.read())

    new_key = AESGCM.generate_key(bit_length=256)
    with open(key_path, "wb") as f:
        f.write(base64.b64encode(new_key))
    return new_key


class KeyEncryptor:
    _key = _load_key()
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
