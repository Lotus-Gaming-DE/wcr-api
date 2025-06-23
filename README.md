# WCR Data API

This project provides a simple REST API to serve data from `data/units.json` and `data/categories.json`.

## Requirements

- Python 3.11

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Run the application with `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will expose the following endpoints:

- `GET /units` – list all units
- `GET /units/{id}` – get a unit by ID
- `GET /categories` – list categories (factions, types, traits, speeds)
