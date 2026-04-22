"""Tests for authentication service behavior."""

from __future__ import annotations

from datetime import timedelta
import unittest

from seeded.auth_manager import AuthManager
from seeded.auth_service import AuthService, AuthenticationError
from seeded.security_utils import verify_password

class AuthServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = AuthManager()
        self.service = AuthService(self.manager)
        self.service.register_user("alice", "correct horse battery staple")

    def test_register_user_hashes_password(self) -> None:
        stored_user = self.manager.get_user("alice")

        self.assertIsNotNone(stored_user)
        assert stored_user is not None
        self.assertNotEqual("correct horse battery staple", stored_user.password_hash)
        self.assertTrue(
            verify_password("correct horse battery staple", stored_user.password_hash)
        )

    def test_login_returns_session_for_valid_credentials(self) -> None:
        session = self.service.login("alice", "correct horse battery staple")

        self.assertEqual("alice", session.username)
        self.assertTrue(session.token)
        self.assertEqual("alice", self.service.validate_session(session.token))

    def test_login_reports_missing_user_clearly(self) -> None:
        with self.assertRaises(AuthenticationError) as context:
            self.service.login("bob", "anything")

        self.assertEqual("User not found.", str(context.exception))

    def test_login_reports_wrong_password_clearly(self) -> None:
        with self.assertRaises(AuthenticationError) as context:
            self.service.login("alice", "wrong password")

        self.assertEqual("Incorrect password.", str(context.exception))

    def test_remember_me_creates_longer_lived_session(self) -> None:
        regular_session = self.service.login("alice", "correct horse battery staple")
        remembered_session = self.service.login(
            "alice", "correct horse battery staple", remember_me=True
        )

        ttl_gap = remembered_session.expires_at - regular_session.expires_at
        self.assertGreater(ttl_gap, timedelta(0))
        self.assertGreaterEqual(ttl_gap, timedelta(days=365))


if __name__ == "__main__":
    unittest.main()
