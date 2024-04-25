from typing import List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings

settings = get_settings()


def test_read_all_drs_yield(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/drs/all")
    assert response.status_code == 200


def test_read_drs_yield_details(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/drs/drs_yield_details")
    assert response.status_code == 200
    data: List[dict] = response.json()
    assert data[0].get("research", None) is not None


def test_read_drs_yield_by_research_id(client: TestClient, db: Session) -> None:
    research = crud.research.get_multi(db)
    research_id = None
    if research:
        for res in research:
            if res.research_type == "Drought-resistant Seeds":
                research_id = res.id
                break

    response = client.get(f"{settings.API_STR}/drs/by_research_id/{research_id}")
    assert response.status_code == 200


def test_read_drs_yield_by_line(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/drs/by_line/R1151AM")
    assert response.status_code == 200

    response = client.get(f"{settings.API_STR}/drs/by_line/wrong_line")
    assert response.status_code == 404
