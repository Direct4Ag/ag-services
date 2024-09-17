"""Pydantic models for representing Fertilizer used in the field"""

import uuid
from datetime import date

from pydantic import BaseModel


class FertilizerBase(BaseModel):
    """Base model for Fertilizer"""

    fertilizer_date: date
    fertilizer_rate: float
    fertilizer_rate_unit: str
    fertilizer_type: str
    fertilizer_application_description: str
    crop_rot_ref_id: uuid.UUID


class FertilizerSummaryInDB(FertilizerBase):
    """Model for Fertilizer in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class FertilizerSummary(FertilizerSummaryInDB):
    pass


class FertilizerCreate(FertilizerBase):
    pass


class FertilizerUpdate(FertilizerBase):
    pass
