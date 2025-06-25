# WCR Data API

[![CI](https://github.com/<owner>/wcr-api/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/wcr-api/actions/workflows/ci.yml)

This project provides a simple REST API to serve data from `data/units.json` and
`data/categories.json`.
Application code resides under `src/wcr_api` following the conventional
`src/` layout.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Requirements

- Python 3.11
- HTTPX for the FastAPI test client (installed via `requirements.txt`)
- Copy `.env.example` to `.env` to customise configuration such as
  ``LOG_LEVEL``.

## Local Development

Install dependencies and start the application with `uvicorn`.
For formatting, linting and running tests install the development requirements:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
PYTHONPATH=src uvicorn main:app --reload
```

Structured logging is initialised during the application's lifespan using
``structlog``. Logs are emitted in JSON format and written both to stdout and
``logs/api.log``. The log level defaults to ``INFO`` but can be changed by
setting the ``LOG_LEVEL`` environment variable (e.g. ``DEBUG``) before starting
the app. The lifespan function also loads unit data on startup so the API is
ready to serve requests immediately.

When running locally the API is available at `http://127.0.0.1:8000`.

### Deployment

Deployments on Railway use the following start command to ensure the
`wcr_api` package is importable:

```bash
PYTHONPATH=src uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Running Tests

Install development dependencies and run the test suite with `python -m pytest`.
Running tests as a module ensures the package imports correctly:

```bash
pip install -r requirements-dev.txt
python -m pytest
```

### Code style

Use `pre-commit` to automatically run Black, Flake8, Ruff and
other basic checks:

```bash
pre-commit install
```

Run all hooks manually with:

```bash
pre-commit run --all-files
```

Continuous integration runs the same hooks and additionally checks
dependencies with `pip-audit`. The Snyk token must be defined as a
repository secret. Pull requests from forks don't receive secrets, so the
Snyk test step is skipped.

### Security scanning

CI installs the Snyk CLI with `snyk/actions/setup@v1` and runs `snyk test`.
The `SNYK_TOKEN` secret must be configured in repository settings. Tests from
forks won't receive this secret, so the Snyk test step is skipped.

### Automatic dependency updates

Dependabot monitors `requirements*.txt` and GitHub Actions workflow files.
Weekly pull requests keep dependencies secure and up to date. Enable
Dependabot alerts in the repository settings to receive notifications about
security issues.

The repository's `.gitignore` excludes environment files, Python bytecode and
pytest cache directories to avoid committing temporary files.

### Data loading

Unit data is loaded once at startup by `DataLoader` via the application's
lifespan context manager which keeps a dictionary for fast lookups. Use
`get_unit_by_id` to retrieve a specific unit without iterating over the entire
list.

If data files cannot be read, the application now returns a 500 JSON response
with `{"detail": "Interner Serverfehler"}` instead of exposing a stack
trace.

## Hosted API

The API is also deployed and accessible under:

```
https://wcr-api.up.railway.app
```

### Available Endpoints

- `GET /units` – list units with optional `offset` and `limit` query params
  (defaults: `offset=0`, `limit=100`, maximum limit `1000`)
- `GET /units/{id}` – get a unit by ID
- `GET /categories` – list categories (factions, types, traits, speeds)

Unit IDs consist of lowercase letters, numbers and hyphens.

All endpoints return JSON.

### Examples

Fetch a subset of units:

```bash
curl "https://wcr-api.up.railway.app/units?offset=0&limit=10"
```

Fetch a single unit:

```bash
curl https://wcr-api.up.railway.app/units/ancient-of-war
```

Fetch categories:

```bash
curl https://wcr-api.up.railway.app/categories
```

#### Example usage in Python

```python
import requests

base_url = "https://wcr-api.up.railway.app"

# list units with pagination
units = requests.get(f"{base_url}/units", params={"offset": 0, "limit": 10}).json()

# single unit by id
unit = requests.get(f"{base_url}/units/ancient-of-war").json()

# categories
categories = requests.get(f"{base_url}/categories").json()
```
