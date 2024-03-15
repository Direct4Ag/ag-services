import json
import logging

import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame
from sqlalchemy import text

from app import PROJECT_ROOT, crud
from app.core.config import get_settings
from app.db import base  # noqa: F401
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Data Import")

settings = get_settings()


class Data:
    def __init__(self) -> None:
        self.db = SessionLocal()

        farm_data_path = PROJECT_ROOT / "data" / "data.json"

        with open(farm_data_path) as f:
            self.data = json.load(f)["dataArray"]

    def insert_data(self) -> None:
        ### truncate all tables
        logger.info("Truncating all tables")
        truncate_query = text("TRUNCATE TABLE farms RESTART IDENTITY CASCADE;")
        self.db.execute(truncate_query)

        for farm in self.data:
            logger.info(f"Importing farm: {farm['name']}")

            ### Insert Farm
            obj_in = {
                "farm_name": farm["name"],
                "location_name": farm["location"],
            }
            # farm_in = schemas.FarmCreate(
            #     **obj_in
            # )  # might cause issue since no ID is provided
            farm_in_db = crud.farm.create(self.db, obj_in=obj_in)

            ### extract polygon data
            field_shapes: GeoDataFrame = gpd.read_file(
                PROJECT_ROOT / "data" / "shapefiles" / farm["polygon"]
            )
            # convert the coordinate reference system to EPSG 4326
            if field_shapes.crs.to_epsg() != 4326:
                field_shapes = field_shapes.to_crs(4326)
                field_shapes["centroid"] = (
                    gpd.GeoSeries.concave_hull(field_shapes)
                    .to_crs("+proj=cea")
                    .centroid.to_crs(4326)
                )

            ### Insert Fields
            for field in farm["fields"]:
                logger.info(f"Importing field: {field['fieldName']}")
                field_shape = str(
                    field_shapes[field_shapes["name"] == field["fieldName"]][
                        "geometry"
                    ].values[0]
                )
                field_coordinate = str(
                    field_shapes[field_shapes["name"] == field["fieldName"]][
                        "centroid"
                    ].values[0]
                )
                obj_in = {
                    "field_name": field["fieldName"],
                    "field_shape": field_shape,
                    "farm_ref_id": farm_in_db.id,
                    "coordinates": field_coordinate,
                }

                field_in_db = crud.field.create(self.db, obj_in=obj_in)

                ### Insert Researches
                logger.info(
                    f"Importing research {field['researchName']} for field: {field['fieldName']}"
                )

                obj_in = {
                    "research_name": field["researchName"],
                    "research_area": field["researchArea"],
                    "research_type": field["researchType"],
                    "field_ref_id": field_in_db.id,
                }

                crud.research.create(self.db, obj_in=obj_in)


if __name__ == "__main__":
    logger.info("Creating initial data")
    data = Data()
    data.insert_data()
    logger.info("Initial data created")
