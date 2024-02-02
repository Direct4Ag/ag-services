"""Pydantic models for representing fields"""

from typing import List
import json

from pydantic import BaseModel, Field, validator
from geoalchemy2 import WKBElement
from shapely.geometry import shape
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
        ret_val = json.loads(v.data)
        coordinate_list = shape(ret_val)
        print(ret_val)
        print(type(coordinate_list))
        return ret_val["coordinates"][0]


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
