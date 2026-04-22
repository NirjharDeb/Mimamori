# Golden Auth Task

This package contains a correct reference implementation of a small Python
authentication task for the Mimamori project.

## Features

- Password hashing and verification
- Secure session token generation
- Short-lived default sessions
- Longer-lived `remember_me` sessions that still expire
- Unit tests for the core authentication flow

## Files

- `auth_service.py`: login and registration behavior
- `auth_manager.py`: in-memory user and session storage
- `security_utils.py`: password and token helpers
- `main.py`: simple demo driver
- `tests/`: unit tests

## Running

From the repository root:

```bash
python -m golden.main
python -m unittest discover -s golden/tests
```
