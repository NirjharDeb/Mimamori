"""Authentication service built on the in-memory auth manager."""

from __future__ import annotations

from golden.auth_manager import AuthManager, SessionRecord, UserRecord
from golden.security_utils import (
    generate_session_token,
    hash_password,
    verify_password,
)

class AuthenticationError(Exception):
    """Raised when authentication fails."""

class AuthService:
    DEFAULT_SESSION_TTL_SECONDS = 60 * 60
    REMEMBER_ME_TTL_SECONDS = 60 * 60 * 24 * 30

    def __init__(self, auth_manager: AuthManager) -> None:
        self._auth_manager = auth_manager

    def register_user(self, username: str, password: str) -> UserRecord:
        password_hash = hash_password(password)
        return self._auth_manager.add_user(username, password_hash)

    def login(
        self, username: str, password: str, *, remember_me: bool = False
    ) -> SessionRecord:
        user = self._auth_manager.get_user(username)
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password.")

        ttl_seconds = (
            self.REMEMBER_ME_TTL_SECONDS
            if remember_me
            else self.DEFAULT_SESSION_TTL_SECONDS
        )
        token = generate_session_token()
        return self._auth_manager.create_session(
            username=user.username,
            token=token,
            ttl_seconds=ttl_seconds,
        )

    def validate_session(self, token: str) -> str | None:
        session = self._auth_manager.get_session(token)
        if session is None:
            return None
        return session.username