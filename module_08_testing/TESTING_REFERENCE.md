# Testing Reference

## Philosophy
Test behavior, not implementation. Keep a fast unit-test core with a thin
layer of integration tests around the ORM and API boundaries.

## Test Pyramid
| Layer | Tool | Speed | Share |
|---|---|---|---|
| Unit (models, utils) | pytest | fast | ~70% |
| Integration (DB, API) | pytest-django, APIClient | medium | ~25% |
| End-to-end | Playwright/Selenium | slow | ~5% |

## Common Commands
    pytest                       # run everything
    pytest -x                    # stop on first failure
    pytest -k "api and create"   # keyword filter
    pytest -m "not slow"         # skip slow markers
    pytest --cov=. --cov-report=html
    pytest -n auto               # parallel (pytest-xdist)

## Fixtures vs Factories
- Fixtures (conftest.py): shared setup wired by name into tests.
- Factories (factory_boy): generate model instances with sane defaults.

## Database
- @pytest.mark.django_db gives a test transactional DB access.
- --reuse-db keeps the test DB between runs for speed.
- Use --create-db to force a rebuild after migrations change.

## Tips
- Prefer factories over fixtures for model data; they read better.
- Freeze time with freezegun for date-sensitive logic.
- Assert on status codes AND response shape for API tests.