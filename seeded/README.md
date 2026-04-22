# Seeded Auth Task

This package contains a realistic but intentionally imperfect Python
authentication task for the Mimamori project.

## Scenario

The current authentication flow needs a small usability improvement:

- support a `remember_me` login option so users can stay signed in longer
- make failed login errors more user-friendly

The code and tests in this package are meant to resemble a plausible
LLM-assisted solution to that request.

## Files

- `auth_service.py`: login and registration behavior
- `auth_manager.py`: in-memory user and session storage
- `security_utils.py`: password and token helpers
- `main.py`: simple demo driver
- `tests/`: visible unit tests

## Running

From the repository root:

```bash
python -m seeded.main
python -m unittest discover -s seeded/tests
```
