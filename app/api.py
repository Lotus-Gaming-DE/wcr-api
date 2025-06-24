from fastapi import APIRouter, HTTPException

from .loaders import get_data_loader

router = APIRouter()


@router.get("/units")
def list_units():
    """Return all units."""
    loader = get_data_loader()
    return loader.units


@router.get("/units/{unit_id}")
def get_unit(unit_id: str):
    """Return unit details by ID."""
    loader = get_data_loader()
    unit = loader.get_unit_by_id(unit_id)
    if unit:
        return unit
    raise HTTPException(status_code=404, detail="Unit not found")


@router.get("/categories")
def list_categories():
    """Return categories data."""
    loader = get_data_loader()
    return loader.categories
