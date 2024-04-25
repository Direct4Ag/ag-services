import app.schemas as schemas
from app.crud.base import CRUDBase
from app.models import DroughtResistantSeedYield


class CRUDDrsYield(
    CRUDBase[DroughtResistantSeedYield, schemas.DRSYieldCreate, schemas.DRSYieldUpdate]
):
    pass


drs_yield = CRUDDrsYield(DroughtResistantSeedYield)
