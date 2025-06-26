"""API route handlers for the WCR Data service."""

from fastapi import APIRouter, HTTPException, Path, Query

from .loaders import get_data_loader

router = APIRouter()


@router.get("/units")
def list_units(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[dict]:
    """Return a slice of the unit list.

    Parameters
    ----------
    offset:
        Number of items to skip from the start of the list. ``0`` by default.
    limit:
        Maximum number of units to return. Values above ``1000`` are rejected.

    Returns
    -------
    list[dict]
        List of unit objects loaded from :mod:`app.loaders`.
    """
    loader = get_data_loader()
    end = offset + limit
    return loader.units[offset:end]


@router.get("/units/{unit_id}")
def get_unit(unit_id: str = Path(..., pattern="^[a-zA-Z0-9-]+$")) -> dict:
    """Return unit details by ID.

    Parameters
    ----------
    unit_id:
        Identifier of the unit. IDs may contain letters, numbers and hyphens.

    Returns
    -------
    dict
        Unit information if found.

    Raises
    ------
    HTTPException
        If no unit with ``unit_id`` exists.
    """
    loader = get_data_loader()
    unit = loader.get_unit_by_id(unit_id)
    if unit:
        return unit
    raise HTTPException(status_code=404, detail="Einheit nicht gefunden")


@router.get("/categories")
def list_categories() -> dict:
    """Return categories data.

    Returns
    -------
    dict
        Mapping of category names to lists of values.
    """
    loader = get_data_loader()
    return loader.categories
