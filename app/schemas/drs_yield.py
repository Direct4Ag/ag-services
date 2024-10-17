"""Pydantic models for representing Drought Resistant Seed Yield"""

import uuid
from datetime import date

from pydantic import BaseModel

from app.schemas.research import ResearchSummary


class DRSYieldBase(BaseModel):
    """Base model for Drought Resistant Seed Yield"""

    replicate: int
    line: str
    planting_date: date
    harvest_date: date
    crop_yield: float
    yield_unit: str


class DRSYieldSummaryInDB(DRSYieldBase):
    """Model for Drought Resistant Seed Yield in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class DRSYieldSummary(DRSYieldSummaryInDB):
    pass


class DRSYieldDetailBase(DRSYieldBase):
    research_ref_id: uuid.UUID


class DRSYieldDetailInDB(DRSYieldDetailBase):
    # research: ResearchDetails
    research: ResearchSummary
    id: uuid.UUID

    class Config:
        orm_mode = True


class DRSYieldDetails(DRSYieldDetailInDB):
    pass


class DRSYieldCreate(DRSYieldDetailBase):
    pass


class DRSYieldUpdate(DRSYieldDetailBase):
    pass
