from pydantic import BaseSettings

import os


class Settings(BaseSettings):
    main_path: str = os.path.abspath(os.path.dirname(__file__))
    models_path: str = os.path.join(main_path, "labels")
    routers_path: str = os.path.join(main_path, "routers")
    postgres_db_url: str = "postgresql://fast:fast@localhost:5432/geostream"


settings = Settings()
