# Seeded Auth Task

This package contains a realistic but intentionally imperfect Python
authentication task for the Mimamori project. Your task is to debug and solve it!

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
