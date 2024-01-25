"""Pydantic models for representing fields"""

from typing import List
import json

from pydantic import BaseModel, Field, validator
from geoalchemy2 import WKBElement
import uuid

from app.schemas.farm import FarmSummary


class FieldBase(BaseModel):
    """Base model for fields"""

    id: uuid.UUID
    field_name: str
    field_shape: List[List[float]] = Field(min_items=1)

    @validator("field_shape", pre=True)
    def to_list(cls, v: WKBElement) -> List[List[float]]:
        """Convert to list"""
        return json.loads(v.data)["coordinates"][0]


class FieldSummaryInDB(FieldBase):
    """Model for farms in DB"""

    class Config:
        orm_mode = True


class FieldSummary(FieldSummaryInDB):
    pass


class FieldDetailBase(FieldBase):
    farm_ref_id: uuid.UUID


class FieldDetailInDB(FieldDetailBase):
    farm: FarmSummary

    class Config:
        orm_mode = True


class FieldDetails(FieldDetailInDB):
    pass


class FieldCreate(FieldDetailBase):
    pass


class FieldUpdate(FieldDetailBase):
    pass
