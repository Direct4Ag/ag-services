from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.FarmSummary])
def read_farm(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve farms."""
    farms = crud.farm.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return farms


@router.get(
    "/{farm_id}",
    response_model=schemas.FarmSummary,
)
def read_farms_by_id(
    farm_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a farm by id."""
    farm = crud.farm.get(db, id=farm_id)
    if not farm:
        raise HTTPException(
            status_code=404, detail=f"Data source not found: ${farm_id}"
        )
    return farm


@router.get("/{farm_id}/fields", response_model=List[schemas.FieldSummary])
def read_farm_fields(
    farm_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the fields for the given farm id."""
    fields = crud.farm.get_fields(db, id=farm_id)
    return fields


@router.post("/", response_model=schemas.FarmSummary)
def create_farm(
    farm_in: schemas.FarmCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create a new farm."""
    farm = crud.farm.create(db, obj_in=farm_in)
    return farm


@router.delete("/{farm_id}", response_model=schemas.FarmSummary)
def delete_farm(
    farm_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete a farm."""
    farm = crud.farm.delete(db, id=farm_id)
    return farm
