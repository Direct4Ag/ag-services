from pydantic import BaseSettings

import os
from typing import Any, Dict, Optional, List, Union
from pydantic import PostgresDsn, validator, AnyHttpUrl


class Settings(BaseSettings):
    main_path: str = os.path.abspath(os.path.dirname(__file__))
    models_path: str = os.path.join(main_path, "../labels")
    routers_path: str = os.path.join(main_path, "../routers")

    ROUTER_PREFIX: str
    PROJECT_NAME: str
    SERVER_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    SERVER_HOST: AnyHttpUrl

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

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
            port=values.get("POSTGRES_PORT"),
            path=f"/{db_name}",
        )


def get_settings() -> Settings:
    return Settings(PROJECT_NAME="Direct4Ag", SERVER_NAME="Direct4Ag API")
