from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Research
from app.schemas import ResearchCreate, ResearchUpdate


class CRUDResearch(CRUDBase[Research, ResearchCreate, ResearchUpdate]):
    def get_research_by(
        self,
        db: Session,
        research_area: Optional[str] = None,
        research_type: Optional[str] = None,
    ) -> List[Research]:
        if research_area is None and research_type is None:
            return self.order_by(
                db.query(Research),
                order_by=["research_name"],
            ).all()
        elif research_area is None:
            return self.order_by(
                db.query(Research).filter(Research.research_type == research_type),
                order_by=["research_name"],
            ).all()
        elif research_type is None:
            return self.order_by(
                db.query(Research).filter(Research.research_area == research_area),
                order_by=["research_name"],
            ).all()

        return self.order_by(
            db.query(Research).filter(
                Research.research_area == research_area,
                Research.research_type == research_type,
            ),
            order_by=["research_name"],
        ).all()


research = CRUDResearch(Research)
