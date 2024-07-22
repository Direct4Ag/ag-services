from typing import List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings

settings = get_settings()


def test_read_all_crop_rotation_yield(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/crop-rotation-yield/all")
    assert response.status_code == 200


def test_read_crop_rotation_yield_details(client: TestClient, db: Session) -> None:
    response = client.get(
        f"{settings.API_STR}/crop-rotation-yield/crop_rotation_details"
    )
    assert response.status_code == 200
    data: List[dict] = response.json()
    assert data[0].get("research", None) is not None


def test_read_drs_yield_by_research_id(client: TestClient, db: Session) -> None:
    research = crud.research.get_multi(db)
    research_id = None
    if research:
        for res in research:
            if res.research_type == "Crop Rotation":
                research_id = res.id
                break

    response = client.get(
        f"{settings.API_STR}/crop-rotation-yield/by_research_id/{research_id}"
    )
    assert response.status_code == 200
