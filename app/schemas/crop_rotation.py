"""Pydantic models for representing Drought Resistant Seed Yield"""

import uuid
from datetime import date

from pydantic import BaseModel

from app.schemas.research import ResearchSummary


class CropRotationBase(BaseModel):
    """Base model for Crop Rotation"""

    planting_date: date
    harvest_date: date
    crop_yield: float
    yield_unit: str
    seeding_rate: float
    seeding_rate_unit: str
    fertilizer_application: str


class CropRotationSummaryInDB(CropRotationBase):
    """Model for Crop Rotation in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class CropRotationSummary(CropRotationSummaryInDB):
    pass


class CropRotationDetailBase(CropRotationBase):
    crop_rot_research_ref_id: uuid.UUID


class CropRotationDetailInDB(CropRotationDetailBase):
    research: ResearchSummary
    id: uuid.UUID

    class Config:
        orm_mode = True


class CropRotationDetails(CropRotationDetailInDB):
    pass


class CropRotationCreate(CropRotationDetailBase):
    pass


class CropRotationUpdate(CropRotationDetailBase):
    pass
