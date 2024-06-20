from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.DRSYieldSummary])
def read_drs_yield(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve all drought resistant seeds yield."""
    drs_yield = crud.drs_yield.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return drs_yield


@router.get("/yield_details", response_model=List[schemas.DRSYieldDetails])
def read_drs_yield_details(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve drought resistant seeds yield."""
    drs_yield = crud.drs_yield.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return drs_yield


@router.get(
    "/by_research_id/{research_id}", response_model=List[schemas.DRSYieldSummary]
)
def read_drs_yield_by_research_id(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get drought resistant seeds yield by research id."""
    drs_yield = crud.drs_yield.order_by(
        db.query(models.DroughtResistantSeedYield).filter(
            models.DroughtResistantSeedYield.research_ref_id == research_id
        ),
        order_by=["line"],
    ).all()
    if not drs_yield:
        raise HTTPException(
            status_code=404,
            detail=f"Drought resistant seeds yield not found for {research_id}",
        )
    return drs_yield


@router.get("/by_line/{line}", response_model=List[schemas.DRSYieldSummary])
def read_drs_yield_by_line(
    line: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get drought resistant seeds yield by line."""
    drs_yield = crud.drs_yield.order_by(
        db.query(models.DroughtResistantSeedYield).filter(
            models.DroughtResistantSeedYield.line == line
        ),
        order_by=["line"],
    ).all()
    if not drs_yield:
        raise HTTPException(
            status_code=404,
            detail=f"Drought resistant seeds yield not found for {line}",
        )
    return drs_yield


@router.post("/", response_model=schemas.DRSYieldDetails)
def create_drs_yield(
    drs_yield_in: schemas.DRSYieldCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create a new drought resistant seeds yield."""
    drs_yield = crud.drs_yield.create(db, obj_in=drs_yield_in)
    return drs_yield


@router.delete("/{drs_yield_id}", response_model=schemas.DRSYieldDetails)
def delete_drs_yield(
    drs_yield_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete a drought resistant seeds yield."""
    drs_yield = crud.drs_yield.delete(db, id=drs_yield_id)
    return drs_yield
