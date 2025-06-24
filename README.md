# WCR Data API

This project provides a simple REST API to serve data from `data/units.json` and
`data/categories.json`.

## Requirements

- Python 3.11

## Local Development

Install dependencies and start the application with `uvicorn`:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

When running locally the API is available at `http://127.0.0.1:8000`.

### Running Tests

Install development dependencies and run the test suite with `pytest`:

```bash
pip install -r requirements-dev.txt
pytest
```

### Data loading

Unit data is loaded once at startup by `DataLoader` which keeps a dictionary
for fast lookups. Use `get_unit_by_id` to retrieve a specific unit without
iterating over the entire list.

## Hosted API

The API is also deployed and accessible under:

```
https://wcr-api.up.railway.app
```

### Available Endpoints

- `GET /units` – list all units
- `GET /units/{id}` – get a unit by ID
- `GET /categories` – list categories (factions, types, traits, speeds)

All endpoints return JSON.

### Examples

Fetch all units:

```bash
curl https://wcr-api.up.railway.app/units
```

Fetch a single unit:

```bash
curl https://wcr-api.up.railway.app/units/abomination
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
unit = requests.get(f"{base_url}/units/abomination").json()

# categories
categories = requests.get(f"{base_url}/categories").json()
```
