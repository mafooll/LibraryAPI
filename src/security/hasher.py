from passlib.context import CryptContext  # type: ignore

from src.common.interfaces.hasher import AbstractPasswordHasher


class PasswordHasher(AbstractPasswordHasher):
    def __init__(self):
        self.context = CryptContext(schemes=['bcrypt'])

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)
