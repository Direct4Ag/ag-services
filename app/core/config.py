import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, PostgresDsn, validator

from app import PROJECT_ROOT


class Settings(BaseSettings):
    """
    API config

    All attributes of this class can be set in the `.env` file in the project root,
    unless they are set as a `const` fields.
    """

    PROJECT_NAME: str = Field("Direct4Ag", const=True)
    SERVER_NAME: str = Field("Direct4Ag API", const=True)

    main_path: str = os.path.abspath(os.path.dirname(__file__))
    models_path: str = os.path.join(main_path, "../labels")
    routers_path: str = os.path.join(main_path, "../routers")

    SERVER_HOST: AnyHttpUrl

    # Set DEBUG = False when in Production else can be set to True.
    DEBUG: bool = False

    API_STR: str = "/api"
    GEOSTREAMS_API_STR: str

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

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str = "test_direct4ag"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    POSTGRES_PORT: str

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

    class Config:
        env_file = PROJECT_ROOT / ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
