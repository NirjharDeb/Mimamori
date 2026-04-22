"""Tests for in-memory user and session storage."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest

from golden.auth_manager import AuthManager
from golden.security_utils import generate_session_token, hash_password


class AuthManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = AuthManager()

    def test_add_user_persists_hashed_password(self) -> None:
        password_hash = hash_password("topsecret")

        user = self.manager.add_user("alice", password_hash)

        self.assertEqual("alice", user.username)
        self.assertEqual(password_hash, user.password_hash)
        self.assertEqual(user, self.manager.get_user("alice"))

    def test_create_session_expires_after_ttl(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        token = generate_session_token()

        session = self.manager.create_session("alice", token, 60, now=now)

        self.assertEqual(now + timedelta(seconds=60), session.expires_at)
        self.assertIsNotNone(
            self.manager.get_session(token, now=now + timedelta(seconds=59))
        )
        self.assertIsNone(
            self.manager.get_session(token, now=now + timedelta(seconds=60))
        )


if __name__ == "__main__":
    unittest.main()
