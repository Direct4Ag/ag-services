import uuid
from datetime import date  # noqa
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Fertilizer, Research


class CropRotation(Base):
    """The Crop Rotation table contains the information about the crop rotation."""

    __tablename__ = "crop_rotation"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    planting_date: date = Column(Date, nullable=False)  # noqa: F811
    harvest_date: date = Column(Date, nullable=False)  # noqa: F811
    crop_yield: float = Column(Float, nullable=True)
    yield_unit: str = Column(String(50), nullable=True)
    seeding_rate: float = Column(Float, nullable=True)
    seeding_rate_unit: str = Column(String(50), nullable=True)
    total_fertilizer_applied: float = Column(Float, nullable=True)
    total_fertilizer_applied_unit: str = Column(String(50), nullable=True)

    crop_rot_research_ref_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("research.id"),
        nullable=False,
    )

    research: "Research" = relationship(
        "Research",
        back_populates="crop_rotation",
        foreign_keys=[crop_rot_research_ref_id],
    )

    fertilizers: List["Fertilizer"] = relationship(
        "Fertilizer",
        back_populates="crop_rotation",
        cascade="all, delete",
    )
