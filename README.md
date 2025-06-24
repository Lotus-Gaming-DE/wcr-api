# WCR Data API

[![CI](https://github.com/OWNER/wcr-data-api/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/wcr-data-api/actions/workflows/ci.yml)

Simple FastAPI service exposing unit and category data loaded from the
`data/` directory. Structured logs are written in JSON to `logs/api.log`
with rotation enabled.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Requirements

- Python 3.11
- `uvicorn` for local development
- see `requirements.txt`

## Development

Install runtime and development dependencies and start the API:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn main:app --reload
```

Install and run pre-commit hooks for formatting and linting:

```bash
pre-commit install
pre-commit run --all-files
```

The configuration uses only local hooks so it works offline once the
development requirements are installed.

Logs are stored in `logs/api.log` and rotated after they reach 1&nbsp;MB.
An example log entry:

```json
{"event": "response", "method": "GET", "path": "/units", "status_code": 200}
```

Run the tests with coverage:

```bash
python -m pytest --cov=app --cov=main
```

## API Endpoints

- `GET /units` – list units with optional `offset` and `limit`
- `GET /units/{id}` – fetch a unit by ID
- `GET /categories` – list category mappings

If data fails to load, the API returns:

```json
{"detail": "Interner Serverfehler"}
```

The API is also deployed at `https://wcr-api.up.railway.app`.
