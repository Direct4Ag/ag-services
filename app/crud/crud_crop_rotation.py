import app.schemas as schemas
from app.crud.base import CRUDBase
from app.models import CropRotation


class CRUDCropRotation(
    CRUDBase[CropRotation, schemas.CropRotationCreate, schemas.CropRotationUpdate]
):
    pass


crop_rotation = CRUDCropRotation(CropRotation)
