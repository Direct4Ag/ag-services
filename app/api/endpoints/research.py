from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.ResearchSummary])
def read_research(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve research."""
    research = crud.research.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return research


@router.get("/{research_id}", response_model=schemas.ResearchDetails)
def read_research_by_id(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a research by id."""
    research = crud.research.get(db, id=research_id)
    if not research:
        raise HTTPException(
            status_code=404, detail=f"Research not found: ${research_id}"
        )
    return research


@router.get("/researchby/", response_model=schemas.ResearchSummary)
def read_research_by(
    research_area: Optional[str] = None,
    research_type: Optional[str] = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get research by research area or research type."""
    research = crud.research.get_research_by(
        db, research_area=research_area, research_type=research_type
    )
    return research
