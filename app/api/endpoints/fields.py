from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=schemas.FieldSummary)
def read_field(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve fields."""
    fields = crud.field.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return fields


@router.get("/{field_id}", response_model=schemas.FieldDetails)
def read_field_by_id(
    field_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a field by id."""
    field = crud.field.get(db, id=field_id)
    if not field:
        raise HTTPException(status_code=404, detail=f"Field not found: ${field_id}")
    return field


@router.get("/{field_id}/research", response_model=List[schemas.ResearchSummary])
def read_field_research(
    field_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the research for the given field id."""
    research = crud.field.get_research(db, id=field_id)
    return research
