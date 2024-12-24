from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """Hash a password for storage."""
    return generate_password_hash(password)


def check_password(stored_password: str, provided_password: str) -> bool:
    """Check if provided password matches the stored hash."""
    return check_password_hash(stored_password, provided_password)
