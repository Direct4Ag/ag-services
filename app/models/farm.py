from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Field


class Farm(Base):
    """The Farm table contains the information about the farm. A farm can have multiple fields"""

    __tablename__ = "farms"

    id: str = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_name: str = Column(String(150), nullable=False)
    location_name: str = Column(String(200), nullable=False)

    fields: List["Field"] = relationship(
        "Field", back_populates="farm", cascade="all, delete"
    )
