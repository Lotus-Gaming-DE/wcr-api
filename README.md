# WCR Data API

[![CI](https://github.com/OWNER/wcr-data-api/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/wcr-data-api/actions/workflows/ci.yml)

This project provides a simple REST API to serve data from `data/units.json` and
`data/categories.json`.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Requirements

- Python 3.11
- HTTPX for the FastAPI test client (installed via `requirements.txt`)

## Local Development

Install dependencies and start the application with `uvicorn`.
For formatting, linting and running tests install the development requirements:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn main:app --reload
```

Logging is configured at **INFO** level on startup so you will see data
loading and request information in the console.

When running locally the API is available at `http://127.0.0.1:8000`.

### Running Tests

Install development dependencies and run the test suite with `pytest`:

```bash
pip install -r requirements-dev.txt
pytest
```

### Code style

Use `pre-commit` to automatically run Black and flake8:

```bash
pre-commit install
```

Run all hooks manually with:

```bash
pre-commit run --all-files
```

The repository's `.gitignore` excludes environment files, Python bytecode and
pytest cache directories to avoid committing temporary files.

### Data loading

Unit data is loaded once at startup by `DataLoader` which keeps a dictionary
for fast lookups. Use `get_unit_by_id` to retrieve a specific unit without
iterating over the entire list.

If data files cannot be read, the application now returns a 500 JSON response
with `{"detail": "Internal server error"}` instead of exposing a stack
trace.

## Hosted API

The API is also deployed and accessible under:

```
https://wcr-api.up.railway.app
```

### Available Endpoints

- `GET /units` – list all units
- `GET /units/{id}` – get a unit by ID
- `GET /categories` – list categories (factions, types, traits, speeds)

Unit IDs consist of lowercase letters, numbers and hyphens.

All endpoints return JSON.

### Examples

Fetch all units:

```bash
curl https://wcr-api.up.railway.app/units
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

# list units
units = requests.get(f"{base_url}/units").json()

# single unit by id
unit = requests.get(f"{base_url}/units/ancient-of-war").json()

# categories
categories = requests.get(f"{base_url}/categories").json()
```
