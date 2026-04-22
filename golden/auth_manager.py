"""In-memory storage for users and sessions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

@dataclass(frozen=True)
class UserRecord:
    username: str
    password_hash: str

@dataclass(frozen=True)
class SessionRecord:
    token: str
    username: str
    expires_at: datetime

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class AuthManager:
    """Manage users and active sessions in memory."""

    def __init__(self) -> None:
        self._users: dict[str, UserRecord] = {}
        self._sessions: dict[str, SessionRecord] = {}

    def add_user(self, username: str, password_hash: str) -> UserRecord:
        if username in self._users:
            raise ValueError(f"User '{username}' already exists.")

        record = UserRecord(username=username, password_hash=password_hash)
        self._users[username] = record
        return record

    def get_user(self, username: str) -> UserRecord | None:
        return self._users.get(username)

    def create_session(
        self,
        username: str,
        token: str,
        ttl_seconds: int,
        *,
        now: datetime | None = None,
    ) -> SessionRecord:
        current_time = now or _utcnow()
        session = SessionRecord(
            token=token,
            username=username,
            expires_at=current_time + timedelta(seconds=ttl_seconds),
        )
        self._sessions[token] = session
        return session

    def get_session(
        self, token: str, *, now: datetime | None = None
    ) -> SessionRecord | None:
        session = self._sessions.get(token)
        if session is None:
            return None

        current_time = now or _utcnow()
        if current_time >= session.expires_at:
            self._sessions.pop(token, None)
            return None

        return session