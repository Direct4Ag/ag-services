import uuid

from pydantic import BaseModel

from app.schemas.field import FieldDetails


class SensorBase(BaseModel):
    """Base model for sensors"""

    depth: str
    sensor_id: int


class SensorSummaryInDB(SensorBase):
    """Model for sensors in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class SensorSummary(SensorSummaryInDB):
    pass


class SensorDetailBase(SensorBase):
    field_ref_id: uuid.UUID


class SensorDetailInDB(SensorDetailBase):
    field: FieldDetails
    id: uuid.UUID

    class Config:
        orm_mode = True


class SensorDetails(SensorDetailInDB):
    pass


class SensorCreate(SensorDetailBase):
    pass


class SensorUpdate(SensorDetailBase):
    pass
