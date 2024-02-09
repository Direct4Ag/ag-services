from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geography
from app.utils.db import Geometry
from geoalchemy2 import WKBElement
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base

# from app.utils.db import Geometry # modify this to geography if required else remove this line

if TYPE_CHECKING:
    from app.models import Farm
    from app.models import Research


class Field(Base):
    """The Fields table contains the information about an individual field. A field can only belong to one farm."""

    __tablename__ = "fields"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_name: str = Column(String(150), nullable=False)
    field_shape: WKBElement = Column(
        Geometry("POLYGON", srid=4326, spatial_index=True), nullable=False
    )

    farm_ref_id: str = Column(
        UUID(as_uuid=True), ForeignKey("farms.id"), nullable=False
    )

    farm: "Farm" = relationship("Farm", back_populates="fields")
    researches: List["Research"] = relationship(
        "Research", back_populates="field", cascade="all, delete"
    )
