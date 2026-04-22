"""Security helpers for password handling and session tokens."""

from __future__ import annotations

import hashlib
import hmac
import secrets

DEFAULT_PBKDF2_ITERATIONS = 100_000
SALT_BYTES = 16
TOKEN_BYTES = 32


def hash_password(password: str, *, iterations: int = DEFAULT_PBKDF2_ITERATIONS) -> str:
    """Return a salted password hash suitable for storage."""
    if not password:
        raise ValueError("Password must not be empty.")

    salt = secrets.token_bytes(SALT_BYTES)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return f"{iterations}${salt.hex()}${derived_key.hex()}"


def verify_password(password: str, stored_password_hash: str) -> bool:
    """Check whether a plaintext password matches a stored hash."""
    try:
        iterations_text, salt_hex, hash_hex = stored_password_hash.split("$", maxsplit=2)
        iterations = int(iterations_text)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
    except (TypeError, ValueError):
        return False

    computed_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return hmac.compare_digest(computed_hash, expected_hash)


def generate_session_token() -> str:
    """Return a high-entropy session token."""
    return secrets.token_urlsafe(TOKEN_BYTES)
