import app.schemas as schemas
from app.crud.base import CRUDBase
from app.models import Fertilizer


class CRUDFertilizer(
    CRUDBase[Fertilizer, schemas.FertilizerCreate, schemas.FertilizerUpdate]
):
    pass


fertilizer = CRUDFertilizer(Fertilizer)
