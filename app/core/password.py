import re

MAX_PASSWORD_BYTES = 72
MIN_PASSWORD_LENGTH = 8


def validate_password_strength(password: str) -> str:
    # Byte-length check (bcrypt requirement)
    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError("Password must be at most 72 bytes")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError("Password must be at least 8 characters long")

    # if not re.search(r"[a-z]", password):
    #     raise ValueError("Password must contain at least one lowercase letter")

    # if not re.search(r"[A-Z]", password):
    #     raise ValueError("Password must contain at least one uppercase letter")

    # if not re.search(r"\d", password):
    #     raise ValueError("Password must contain at least one digit")

    # if not re.search(r"[^\w\s]", password):
    #     raise ValueError("Password must contain at least one special character")

    if password.strip() != password:
        raise ValueError("Password cannot start or end with whitespace")

    return password
