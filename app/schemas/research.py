"""Pydantic models for representing fields"""

from pydantic import BaseModel
import uuid

from app.schemas.field import FieldDetails


class ResearchBase(BaseModel):
    """Base model for researches"""

    id: uuid.UUID
    research_name: str
    research_area: str
    research_type: str


class ResearchSummaryInDB(ResearchBase):
    """Model for research in DB"""

    class Config:
        orm_mode = True


class ResearchSummary(ResearchSummaryInDB):
    pass


class ResearchDetailBase(ResearchBase):
    field_ref_id: uuid.UUID


class ResearchDetailInDB(ResearchDetailBase):
    field: FieldDetails
    # field: FieldSummary

    class Config:
        orm_mode = True


class ResearchDetails(ResearchDetailInDB):
    pass


class ResearchCreate(ResearchDetailBase):
    pass


class ResearchUpdate(ResearchDetailBase):
    pass
