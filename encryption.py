import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto:
    __backend = default_backend()
    __iterations = 100_000

    #  Encrypted token to my bot
    __encrypted_token = b'pa7ILioXcGYyksfXWVYSZgABhqCAAAAAAGRaYRBEYnnulcXaTu' \
                        b'xcvimy6Rrn7snffE08MwcUOAgfE_iLnc084P0uigQ9aPaOOX1YTZr' \
                        b'rGaXLfQB5Gs1FV7Hp2J1EU1Io7xZnKmR_6heHBnr4XlNdZIQEccY2J082BSaUZy8='

    @staticmethod
    def get_token(password: str):
        return Crypto.__password_decrypt(Crypto.__encrypted_token, password).decode()

    @staticmethod
    def __derive_key(password: bytes, salt: bytes) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=Crypto.__iterations, backend=Crypto.__backend)
        return b64e(kdf.derive(password))

    @staticmethod
    def __password_encrypt(message: bytes, password: str) -> bytes:
        salt = secrets.token_bytes(16)
        key = Crypto.__derive_key(password.encode(), salt, Crypto.__iterations)
        return b64e(
            b'%b%b%b' % (
                salt,
                Crypto.__iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        )

    @staticmethod
    def __password_decrypt(token: bytes, password: str) -> bytes:
        decoded = b64d(token)
        salt, token = decoded[:16], b64e(decoded[20:])
        key = Crypto.__derive_key(password.encode(), salt)
        return Fernet(key).decrypt(token)
