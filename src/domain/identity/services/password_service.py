import bcrypt


class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        password_byte = password.encode()
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=password_byte, salt=salt).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        hashed_password_byte = hashed_password.encode()
        password_byte = password.encode()
        return bcrypt.checkpw(
            password=password_byte, hashed_password=hashed_password_byte
        )


def get_password_service() -> PasswordService:
    return PasswordService()
