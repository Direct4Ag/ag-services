from pydantic import BaseSettings

import os
from typing import Any, Dict, Optional
from pydantic import PostgresDsn, validator


class Settings(BaseSettings):
    main_path: str = os.path.abspath(os.path.dirname(__file__))
    models_path: str = os.path.join(main_path, "labels")
    routers_path: str = os.path.join(main_path, "routers")

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # TODO remove this later once service API is ready - this disables fetching the models
    LOAD_MODELS: bool = False

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        db_name = values.get(
            "POSTGRES_TEST_DB" if os.environ.get("PYTHON_TEST") else "POSTGRES_DB", ""
        )
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{db_name}",
        )


settings = Settings()
