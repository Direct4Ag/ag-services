from typing import List

from sqlalchemy.orm import Session
import json
from geoalchemy2.functions import ST_AsGeoJSON

from app.crud.base import CRUDBase
from app.models import Field, Research

from app.schemas import FieldCreate, FieldUpdate


class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    def get_research(self, db: Session, id: str) -> List[Research]:
        return self.order_by(
            db.query(Research).filter(Research.field_ref_id == id),
            order_by=["research_area"],
        ).all()

    def get_field_geojson(self, db: Session) -> dict:
        # Use ST_AsGeoJSON function to convert the geometry column to GeoJSON
        query = db.query(
            Field.id,
            Field.field_name,
            ST_AsGeoJSON(Field.field_shape).label("shape_jeojson"),
        ).all()

        # Create and return GeoJSON response
        geojson_response = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": json.loads(row.shape_jeojson),
                    "properties": {
                        "id": str(row.id),
                        "name": row.field_name,
                        # Add more properties as needed
                    },
                }
                for row in query
            ],
        }

        return geojson_response


field = CRUDField(Field)
