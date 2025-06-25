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
- Environment-based log level via ``LOG_LEVEL`` variable.
- Rotating file handler writing logs to ``logs/api.log``.
- Security scan in CI with ``pip-audit``.
- Snyk security scanning step in CI workflow.
- ``SNYK_TOKEN`` documented in ``.env.example`` for CI.
- Additional pre-commit hooks (Ruff, check-yaml, trailing-whitespace,
  end-of-file-fixer).
- Dependabot configuration for Python and GitHub Actions updates.
- Example ``.env.example`` file.
- Project moved to ``src/wcr_api`` package layout.

### Changed
- Unit ID path parameter now accepts hyphenated IDs.
- Startup now uses a FastAPI lifespan function instead of a deprecated
  ``@app.on_event`` handler.
- README instructions for running tests with ``python -m pytest`` and corrected
  the Available Endpoints header.
- Railway start command now sets ``PYTHONPATH=src`` before launching ``uvicorn``.
- Error response for data load failures now returns German message
  ``{"detail": "Interner Serverfehler"}``.

### Removed
- Empty `app/__init__.py` module as namespace packages are supported.

## [0.1.0] - 2025-06-24
### Added
- FastAPI API serving units and categories.
- `DataLoader` for cached lookups.
- Pre-commit hooks and CI workflow.
### Changed
- Updated dependencies: FastAPI, Uvicorn and httpx.
