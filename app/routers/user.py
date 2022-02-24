from typing import List, Optional

import databases
import sqlalchemy
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings

# database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
database = databases.Database("postgresql://fast:fast@localhost:5432/geostream")

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("gid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("emailconfirmed", sqlalchemy.Boolean),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("organization", sqlalchemy.String),
    sqlalchemy.Column("services", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    settings.SQLALCHEMY_DATABASE_URI)
metadata.create_all(engine)

router = APIRouter(
    prefix="/user/api",
    tags=["users"],
    dependencies=[],
    responses={},
)


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    organization: str


class UserOut(BaseModel):
    gid: Optional[int]
    first_name: str
    last_name: str
    email: str
    emailconfirmed: bool
    organization: str
    services: str


class User(BaseModel):
    gid: int
    email: str
    emailconfirmed: bool
    password: str
    first_name: str
    last_name: str
    organization: str
    services: str


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@router.get("/users/", response_model=List[UserOut])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@router.get("/users/{gid}", response_model=UserOut)
async def read_users(*, gid: int):
    query = f"SELECT * FROM users WHERE users.gid={gid};"
    user = await database.fetch_all(query)
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]


@router.post("/users/", response_model=UserIn)
async def create_user(user: UserIn):
    query = users.insert().values(email=user.email, emailconfirmed=False,
                                  password="$2a$10$L7NjWeiZsY92KdEf5kM9q.5s7VTabvKL6vkGYOhg7ufJaWO.S5dYG",
                                  first_name=user.first_name, last_name=user.last_name, organization=user.organization,
                                  services="serviceDownload")
    gid = await database.execute(query)
    return {**user.dict(), "gid": gid}
