# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Expanded docstrings for `DataLoader` and API endpoints.
- Initial changelog tracking features and dependency updates.
- .gitignore entries for environment files, compiled Python and test cache.

### Changed
- Unit ID path parameter now accepts hyphenated IDs.
- Startup now uses a FastAPI lifespan function instead of a deprecated
  ``@app.on_event`` handler.

### Removed
- Empty `app/__init__.py` module as namespace packages are supported.

## [0.1.0] - 2025-06-24
### Added
- FastAPI API serving units and categories.
- `DataLoader` for cached lookups.
- Pre-commit hooks and CI workflow.
### Changed
- Updated dependencies: FastAPI, Uvicorn and httpx.
