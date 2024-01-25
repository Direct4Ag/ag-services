from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Field, Research

from app.schemas import FieldCreate, FieldUpdate


class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    def get_research(self, db: Session, id: str) -> List[Research]:
        return self.order_by(
            db.query(Research).filter(Research.field_ref_id == id),
            order_by=["research_area"],
        ).all()


field = CRUDField(Field)
