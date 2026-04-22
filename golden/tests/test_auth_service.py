"""Tests for authentication service behavior."""

from __future__ import annotations

from datetime import timedelta
import unittest

from golden.auth_manager import AuthManager
from golden.auth_service import AuthService, AuthenticationError
from golden.security_utils import hash_password, verify_password


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

    def test_login_uses_generic_error_for_missing_user(self) -> None:
        with self.assertRaises(AuthenticationError) as context:
            self.service.login("bob", "anything")

        self.assertEqual("Invalid username or password.", str(context.exception))

    def test_login_uses_generic_error_for_wrong_password(self) -> None:
        with self.assertRaises(AuthenticationError) as context:
            self.service.login("alice", "wrong password")

        self.assertEqual("Invalid username or password.", str(context.exception))

    def test_remember_me_creates_longer_lived_session(self) -> None:
        regular_session = self.service.login("alice", "correct horse battery staple")
        remembered_session = self.service.login(
            "alice", "correct horse battery staple", remember_me=True
        )

        regular_ttl = regular_session.expires_at - remembered_session.expires_at
        self.assertLess(regular_ttl, timedelta(0))
        self.assertEqual(
            AuthService.REMEMBER_ME_TTL_SECONDS - AuthService.DEFAULT_SESSION_TTL_SECONDS,
            int(abs(regular_ttl.total_seconds())),
        )

    def test_hash_password_outputs_verifiable_hash(self) -> None:
        password_hash = hash_password("another secret")

        self.assertTrue(verify_password("another secret", password_hash))
        self.assertFalse(verify_password("not it", password_hash))


if __name__ == "__main__":
    unittest.main()
