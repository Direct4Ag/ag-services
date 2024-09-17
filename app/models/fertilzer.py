import uuid
from datetime import date  # noqa
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import CropRotation


class Fertilizer(Base):
    """Fertilizer table contains the information about the fertilizer used in the field."""

    __tablename__ = "fertilizer"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fertilizer_date: date = Column(Date, nullable=False)  # noqa: F811
    fertilizer_rate: float = Column(Float, nullable=False)
    fertilizer_rate_unit: str = Column(String(50), nullable=False)
    fertilizer_type: str = Column(String(200), nullable=False)
    fertilizer_application_description: str = Column(Text, nullable=False)

    crop_rot_ref_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("crop_rotation.id"),
        nullable=False,
    )

    crop_rotation: "CropRotation" = relationship(
        "CropRotation",
        back_populates="fertilizers",
        foreign_keys=[crop_rot_ref_id],
    )
