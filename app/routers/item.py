from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Path

from pydantic import BaseModel

router = APIRouter(
    prefix="/item/api",
    tags=["items"],
    dependencies=[],
    responses={},
)


class Item(BaseModel):
    item_id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


fake_items_db = {"item_id": 1}, {"item_id": 2}, {"item_id": 3}


@router.get("/items")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@router.get("/items/{item_id}")
async def read_item(
        *, item_id: int = Path(..., title="The ID of the item", ge=1, le=1000),

):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]


@router.post("/items/")
async def create_item(item: Item):
    return item
