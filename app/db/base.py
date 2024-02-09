# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.farm import Farm  # noqa
from app.models.field import Field  # noqa
from app.models.research import Research  # noqa
