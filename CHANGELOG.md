# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Expanded docstrings for `DataLoader` and API endpoints.
- `DataLoader.load` now reports malformed JSON via `DataLoadError`.
- Test case for invalid `units.json` to ensure `DataLoadError` is raised.
- Coverage reporting in CI with `pytest-cov` and uploaded artifact.
- Initial changelog tracking features and dependency updates.
- .gitignore entries for environment files, compiled Python and test cache.
- Structured JSON logging with ``structlog`` and request/response middleware.
- Test coverage for the logging middleware.
- Pagination for ``GET /units`` via ``offset`` and ``limit`` query parameters.
- Rotating file logging under ``logs/api.log`` with retention.
- Pre-commit hooks for Ruff, YAML checks and whitespace cleanup.
- Test ensuring log file creation on startup.
- Ruff added to development requirements.
- Local hook configuration to avoid network access during CI.

### Changed
- Unit ID path parameter now accepts hyphenated IDs.
- Startup now uses a FastAPI lifespan function instead of a deprecated
  ``@app.on_event`` handler.
- README instructions for running tests with ``python -m pytest`` and corrected
  the Available Endpoints header.
- Data loader error message now returned in German.

### Removed
- Empty `app/__init__.py` module as namespace packages are supported.

## [0.1.0] - 2025-06-24
### Added
- FastAPI API serving units and categories.
- `DataLoader` for cached lookups.
- Pre-commit hooks and CI workflow.
### Changed
- Updated dependencies: FastAPI, Uvicorn and httpx.
