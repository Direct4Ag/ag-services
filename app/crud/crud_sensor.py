import app.schemas as schemas
from app.crud.base import CRUDBase
from app.models import Sensors


class CRUDSensor(CRUDBase[Sensors, schemas.SensorCreate, schemas.SensorUpdate]):
    pass


sensor = CRUDSensor(Sensors)
