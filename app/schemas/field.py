"""Pydantic models for representing fields"""

from typing import List
import json

from pydantic import BaseModel, Field, validator
from geoalchemy2 import WKBElement

from app.schemas.farm import FarmSummary


class FieldBase(BaseModel):
    """Base model for fields"""

    id: str
    field_name: str
    location: List[List[float]] = Field(min_items=1)

    @validator("location", pre=True)
    def to_list(cls, v: WKBElement) -> List[List[float]]:
        """Convert to list"""
        print(type(v))
        print(v)
        return json.loads(v.data)["location"]


class FieldSummaryInDB(FieldBase):
    """Model for farms in DB"""

    class Config:
        orm_mode = True


class FieldSummary(FieldSummaryInDB):
    pass


class FieldDetailBase(FieldBase):
    farm_ref_id: str


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
