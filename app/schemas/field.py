"""Pydantic models for representing fields"""

import json
import uuid
from typing import List

from geoalchemy2 import WKBElement
from pydantic import BaseModel, Field, validator
from shapely.geometry import shape

from app.schemas.farm import FarmSummary


class FieldBase(BaseModel):
    """Base model for fields"""

    id: uuid.UUID
    field_name: str
    coordinates: List[float] = Field(min_items=2, max_items=2)

    @validator("coordinates", pre=True)
    def to_point(cls, value: WKBElement) -> List[float]:
        """Convert the WKBElement received from SQLAlchemy to a list of long and lat."""
        return json.loads(value.data)["coordinates"]


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


class FieldGeoJSON(BaseModel):
    """Model for fields in GeoJSON format"""

    type: str = "FeatureCollection"
    features: List[dict]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
