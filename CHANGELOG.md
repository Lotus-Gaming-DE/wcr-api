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
- Pre-commit hook for ``pip-audit`` using CycloneDX SBOM support.
- CI: CycloneDX SBOM generation uploaded as `sbom.xml` artifact.
- CI: Use `snyk/actions/setup@v1`; fixed action not found errors.
- CI: Added SNYK_TOKEN env for Snyk Test; clarified fork tests won't have secrets.
- CI: Skip Snyk test in forked PRs to prevent missing-secret auth errors.
- Additional pre-commit hooks (Ruff, check-yaml, trailing-whitespace,
  end-of-file-fixer).
- Dependabot configuration for Python and GitHub Actions updates.
- Documentation sections describing Dependabot usage and Snyk scanning via
  `SNYK_TOKEN`.
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
- CI caches pre-commit hooks for faster runs.
- CI streams Railway logs to `logs/latest_railway.log` and uploads the file as
  an artifact.
- CI caches pip downloads alongside pre-commit hooks for faster builds.
- Documented Dependabot's daily update mechanism and CI caching in README.
- Dependabot update schedule changed to daily.
- Pinned `pip-audit` to version 2.9.0 for consistent SBOM generation.

### Removed
- Empty `app/__init__.py` module as namespace packages are supported.

## [0.1.0] - 2025-06-24
### Added
- FastAPI API serving units and categories.
- `DataLoader` for cached lookups.
- Pre-commit hooks and CI workflow.
### Changed
- Updated dependencies: FastAPI, Uvicorn and httpx.
