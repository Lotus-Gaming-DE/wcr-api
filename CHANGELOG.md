# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.2.0] - 2025-06-24
### Added
- Adopted `src/` layout under `wcr_data_api` package.
- Extended pre-commit with Ruff and formatting hooks.
- CI now caches dependencies and runs `pip-audit`.
- Added MIT LICENSE and `.env.example`.
- Logs stored in `logs/` with rotation policy.
### Changed
- Documentation updated for new package path and tooling.

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

### Changed
- Unit ID path parameter now accepts hyphenated IDs.
- Startup now uses a FastAPI lifespan function instead of a deprecated
  ``@app.on_event`` handler.
- README instructions for running tests with ``python -m pytest`` and corrected
  the Available Endpoints header.

### Removed
- Empty `app/__init__.py` module as namespace packages are supported.

## [0.1.0] - 2025-06-24
### Added
- FastAPI API serving units and categories.
- `DataLoader` for cached lookups.
- Pre-commit hooks and CI workflow.
### Changed
- Updated dependencies: FastAPI, Uvicorn and httpx.
