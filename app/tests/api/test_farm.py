import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings

settings = get_settings()


def test_read_all_farms(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/farms/all")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "skip",
    [
        0,
    ],
)
def test_read_farm_by_id(client: TestClient, skip: int, db: Session) -> None:
    farms = crud.farm.get_multi(db, skip=skip, limit=1)
    farm_id = None
    if farms:
        farm_id = farms[0].id

    response = client.get(f"{settings.API_STR}/farms/{farm_id}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "skip",
    [
        0,
    ],
)
def test_read_fieds_by_farm_id(client: TestClient, skip: int, db: Session) -> None:
    farms = crud.farm.get_multi(db, skip=skip, limit=1)
    farm_id = None
    if farms:
        farm_id = farms[0].id

    response = client.get(f"{settings.API_STR}/farms/{farm_id}/fields")
    assert response.status_code == 200
