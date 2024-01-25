"""Pydantic models for representing farms"""

from typing import List

from pydantic import BaseModel
import uuid


class FarmBase(BaseModel):
    """Base model for farms"""

    id: uuid.UUID
    farm_name: str
    location_name: str


class FarmSummaryInDB(FarmBase):
    """Model for farms in DB"""

    class Config:
        orm_mode = True


class FarmSummary(FarmSummaryInDB):
    pass


class FarmCreate(FarmBase):
    pass


class FarmUpdate(FarmBase):
    pass
