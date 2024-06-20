import uuid
from datetime import date  # noqa
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Research


class DroughtResistantSeedYield(Base):
    """The Drought Resistant Seed Yield table contains the information about the yield of the drought resistant seeds."""

    __tablename__ = "drought_resistant_seed_yield"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    replicate: int = Column(Integer, nullable=True)
    line: str = Column(String(200), nullable=False)
    planting_date: date = Column(Date, nullable=False)  # noqa: F811
    harvest_date: date = Column(Date, nullable=False)  # noqa: F811
    crop_yield: float = Column(Float, nullable=True)

    research_ref_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("research.id"),
        nullable=False,
    )

    research: "Research" = relationship(
        "Research", back_populates="drought_resistant_seed_yield", cascade="all, delete"
    )
