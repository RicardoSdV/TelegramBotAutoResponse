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
    __encrypted_token: bytes = b'pa7ILioXcGYyksfXWVYSZgABhqCAAAAAAGRaYRBEYnnulcXaTu' \
                               b'xcvimy6Rrn7snffE08MwcUOAgfE_iLnc084P0uigQ9aPaOOX1YTZr' \
                               b'rGaXLfQB5Gs1FV7Hp2J1EU1Io7xZnKmR_6heHBnr4XlNdZIQEccY2J082BSaUZy8='

    # Encrypted name of my bot
    __encrypted_bot_name: bytes = b'FSCqUqDGpkWnyVFj9W3s5AABhqCAAAAAAGRbwS4v2EoIlw3RmAxoVdCbOLdzHoww' \
                                  b'SxTulFjAcDOA4Fo4vWaUqkjNYY3vXKdkIXqyQ6lWbC9ogLELMUglQokHV9aTGI7j5h' \
                                  b'X6jrvyBvbLAYlgVg=='

    @staticmethod
    def __password_decrypt(encryption: bytes, password: str) -> str | None:
        try:
            decoded = b64d(encryption)
            salt, encryption = decoded[:16], b64e(decoded[20:])
            key = Crypto.__derive_key(password.encode(), salt)
            return Fernet(key).decrypt(encryption).decode()
        except:
            return None

    @staticmethod
    def get_token(password: str) -> str | None:
        return Crypto.__password_decrypt(Crypto.__encrypted_token, password)

    @staticmethod
    def get_bot_name(password: str) -> str | None:
        return Crypto.__password_decrypt(Crypto.__encrypted_bot_name, password)

    @staticmethod
    def __derive_key(password: bytes, salt: bytes) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=Crypto.__iterations, backend=Crypto.__backend)
        return b64e(kdf.derive(password))

    @staticmethod
    def password_encrypt(message: bytes, password: str) -> bytes:
        salt = secrets.token_bytes(16)
        key = Crypto.__derive_key(password.encode(), salt)
        return b64e(
            b'%b%b%b' % (
                salt,
                Crypto.__iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        )
