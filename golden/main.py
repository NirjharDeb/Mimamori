"""Simple driver script for the golden authentication task."""

from __future__ import annotations

from golden.auth_manager import AuthManager
from golden.auth_service import AuthService, AuthenticationError

def build_demo_service() -> AuthService:
    auth_manager = AuthManager()
    auth_service = AuthService(auth_manager)
    auth_service.register_user("alice", "correct horse battery staple")
    return auth_service

def main() -> None:
    auth_service = build_demo_service()

    print("Attempting successful login...")
    session = auth_service.login(
        "alice", "correct horse battery staple", remember_me=True
    )
    print(f"Logged in as {session.username}")
    print(f"Session token: {session.token}")
    print(f"Expires at: {session.expires_at.isoformat()}")

    print("\nAttempting failed login...")
    try:
        auth_service.login("alice", "wrong password")
    except AuthenticationError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
