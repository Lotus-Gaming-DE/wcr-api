# WCR Data API

[![CI](https://github.com/Lotus-Gaming-DE/wcr-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Lotus-Gaming-DE/wcr-api/actions/workflows/ci.yml)

## Overview

This project provides a simple REST API to serve data from
`data/units.json` and `data/categories.json`. Application code lives under
`src/wcr_api` following the conventional `src/` layout.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Setup

- Python 3.11
- HTTPX for the FastAPI test client (installed via `requirements.txt`)
- Copy `.env.example` to `.env` to customise configuration such as
  ``LOG_LEVEL``.

Install dependencies and start the application with `uvicorn`. For
formatting, linting and running tests install the development requirements:

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

## Utility Scripts

Run `python scripts/fetch_data.py --help` to download the latest unit and
category data from the deployed API. By default the script writes the JSON files
to the `data/` directory.

## Usage

When running locally the API is available at `http://127.0.0.1:8000`.

## Tests

Install development dependencies and run the test suite with coverage enabled.
Running tests as a module ensures the package imports correctly and collects
coverage metrics:

```bash
pip install -r requirements-dev.txt
python -m pytest --cov=. --cov-report=term-missing:skip-covered
```

## Deployment

Deployments on Railway use the following start command to ensure the
`wcr_api` package is importable:

```bash
PYTHONPATH=src uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Code style

Use `pre-commit` to automatically run Black, Flake8, Ruff,
`pip-audit` and other basic checks:

```bash
pre-commit install
```

Run all hooks manually with:

```bash
pre-commit run --all-files
```

The `pip-audit` hook (version `2.9.0`) scans `requirements.txt` and
outputs a column formatted report. It installs `pip-audit[cyclonedx]`
and `cyclonedx-bom` so CI can generate a CycloneDX software bill of
 materials. CI installs the Railway CLI from `@railway/cli`, which
 automatically authenticates via the `RAILWAY_TOKEN` environment variable,
 runs the same
hooks, and then streams Railway logs with
`railway logs --follow > logs/latest_railway.log` which is uploaded as a
build artifact.
If more logs are needed, trigger the `Railway Logs` workflow from the Actions
tab to capture production logs for the `bot` service.

### Security scanning

CI installs the Snyk CLI via `npm install -g snyk` and runs `snyk test`.
Authentication is provided via the `SNYK_TOKEN` environment variable set as a
repository secret. Pull requests from forks do not receive secrets, therefore
the Snyk step is skipped in that scenario.

### Automatic dependency updates

Dependabot checks `requirements*.txt` and workflow files as configured in
`.github/dependabot.yml`. Python dependencies are updated daily while GitHub
Actions workflows are updated weekly. Dependabot pull requests trigger the full
CI pipeline with linting, tests and `pip-audit`. These updates run the same
workflow as any other pull request ensuring quality gates are met. CI caches
pip downloads and pre-commit hooks for faster runs and stores build logs under
`logs/`. Enable Dependabot alerts in repository settings to receive security
notifications.

The repository's `.gitignore` excludes environment files, Python bytecode,
pytest cache directories and the `data/` folder to avoid committing temporary
files.

### Data loading

Unit data is loaded once at startup by `DataLoader` via the application's
lifespan context manager which keeps a dictionary for fast lookups. Use
`get_unit_by_id` to retrieve a specific unit without iterating over the entire
list.

If data files cannot be read, the application now returns a 500 JSON response
with `{"detail": "Interner Serverfehler"}` instead of exposing a stack
trace. Requests for unknown unit IDs return a 404 response containing
`{"detail": "Einheit nicht gefunden"}`.

### Data files

Example JSON data for local development resides in `data/units.json` and
`data/categories.json`. The `data/` directory is gitignored so you can replace
these files without committing them. Use the `fetch_data.py` utility to refresh
the contents:

```bash
python scripts/fetch_data.py
```

### Hosted API

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
