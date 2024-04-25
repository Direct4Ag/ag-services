import argparse
import datetime
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

parser = argparse.ArgumentParser()
parser.add_argument("--testing", action="store_true")
args = parser.parse_args()


def parse_date(date_string):
    """
    Converts a date string in 'MM/DD/YY' format to a datetime.date object.

    Args:
    date_string (str): The date string to parse, expected in 'MM/DD/YY' format.

    Returns:
    datetime.date: A date object representing the parsed date.

    Raises:
    ValueError: If the date_string is not in the expected format or is invalid.
    """
    # Parse the date string using strptime with the appropriate format
    try:
        date_object = datetime.datetime.strptime(date_string, "%m/%d/%y").date()
        return date_object
    except ValueError as e:
        # Raise an error with a more descriptive message
        raise ValueError(
            f"Invalid date or format: {date_string}. Expected format is MM/DD/YY."
        ) from e


class Data:
    def __init__(self, test_mode: bool) -> None:
        self.db = SessionLocal()

        self.data_path = PROJECT_ROOT / ("data" if not test_mode else "test_data")
        farm_data_path = self.data_path / "data.json"

        with open(farm_data_path) as f:
            self.data = json.load(f)["dataArray"]

    def insert_data(self) -> None:
        # truncate all tables
        logger.info("Truncating all tables")
        truncate_query = text("TRUNCATE TABLE farms RESTART IDENTITY CASCADE;")
        self.db.execute(truncate_query)

        for farm in self.data:
            logger.info(f"Importing farm: {farm['name']}")

            # Insert Farm
            obj_in = {
                "farm_name": farm["name"],
                "location_name": farm["location"],
            }
            # farm_in = schemas.FarmCreate(
            #     **obj_in
            # )  # might cause issue since no ID is provided
            farm_in_db = crud.farm.create(self.db, obj_in=obj_in)

            # extract polygon data
            field_shapes: GeoDataFrame = gpd.read_file(
                self.data_path / "shapefiles" / farm["polygon"]
            )
            # convert the coordinate reference system to EPSG 4326
            if field_shapes.crs.to_epsg() != 4326:
                field_shapes = field_shapes.to_crs(4326)

            field_shapes["centroid"] = (
                gpd.GeoSeries.concave_hull(field_shapes)
                .to_crs("+proj=cea")
                .centroid.to_crs(4326)
            )

            # Insert Fields
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

                # Insert Researches
                logger.info(
                    f"Importing research {field['researchName']} for field: {field['fieldName']}"
                )

                obj_in = {
                    "research_name": field["researchName"],
                    "research_area": field["researchArea"],
                    "research_type": field["researchType"],
                    "field_ref_id": field_in_db.id,
                }

                research = crud.research.create(self.db, obj_in=obj_in)

                # Insert Drought Resistant Seed Data if available
                if len(field["drs_yield_data"]) != 0:
                    logger.info(
                        f"Importing DRS Yield Data for research: {field['researchName']}"
                    )
                    for drs_yield in field["drs_yield_data"]:
                        obj_in = {
                            "replicate": drs_yield["replicate"],
                            "line": drs_yield["line"],
                            "planting_date": parse_date(drs_yield["planting_date"]),
                            "harvest_date": parse_date(drs_yield["harvest_date"]),
                            "yield_amount": drs_yield["yield_amount"],
                            "research_ref_id": research.id,
                        }

                # Insert Sensors
                for sensor in field["sensors"]:
                    logger.info(
                        f"Importing sensor {sensor['sensorId']} for field: {field['fieldName']}"
                    )
                    obj_in = {
                        "depth": sensor["depth"],
                        "sensor_id": sensor["sensorId"],
                        "field_ref_id": field_in_db.id,
                    }

                    crud.sensor.create(self.db, obj_in=obj_in)


if __name__ == "__main__":
    logger.info("Creating initial data")
    data = Data(test_mode=args.testing)
    data.insert_data()
    logger.info("Initial data created")
