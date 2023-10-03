# from typing import List, Optional
#
# import databases
# import sqlalchemy
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
#
# from app.core.config import settings
#
# database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
#
# metadata = sqlalchemy.MetaData()
#
# fields = sqlalchemy.Table(
#     "fields",
#     metadata,
#     sqlalchemy.Column("field_id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("name", sqlalchemy.String),
#     sqlalchemy.Column("lat", sqlalchemy.String),
#     sqlalchemy.Column("lon", sqlalchemy.String),
#     sqlalchemy.Column("crop", sqlalchemy.String),
#
# )
#
# engine = sqlalchemy.create_engine(
#     settings.SQLALCHEMY_DATABASE_URI)
# metadata.create_all(engine)
#
# router = APIRouter(
#     prefix="/field/api",
#     tags=["fields"],
#     dependencies=[],
#     responses={},
# )
#
#
# class Field(BaseModel):
#     field_id: Optional[int]
#     name: str
#     lat: str
#     lon: str
#     crop: str
#
#
# @router.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @router.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#
#
# @router.get("/fields/", response_model=List[Field])
# async def read_fields():
#     query = fields.select()
#     return await database.fetch_all(query)
#
#
# @router.get("/fields/{field_id}", response_model=Field)
# async def read_field(*, field_id: int):
#     query = f"SELECT * FROM fields WHERE fields.field_id={field_id};"
#     field = await database.fetch_all(query)
#     if len(field) == 0:
#         raise HTTPException(status_code=404, detail="Field not found")
#     return field[0]
#
#
# @router.delete("/fields/{field_id}")
# async def delete_field(*, field_id: int):
#     query = f"DELETE FROM fields WHERE fields.field_id={field_id} RETURNING *;"
#     deleted = await database.fetch_all(query)
#     if len(deleted) == 0:
#         raise HTTPException(status_code=404, detail="Field not found")
#     return f"Field with id {field_id} was deleted successfully."
#
#
# @router.post("/fields/", response_model=Field)
# async def create_field(field: Field):
#     query = fields.insert().values(name=field.name, lat=field.lat, lon=field.lon, crop=field.crop)
#     field_id = await database.execute(query)
#     return {**field.dict(), "field_id": field_id}
