from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

settings = (
    get_settings()
)  # Get the Settings object with all the environment information

app = FastAPI(title=settings.SERVER_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()

app.include_router(api_router, prefix=settings.ROUTER_PREFIX)


@app.get("/direct4ag")
async def root():
    return {"message": "Welcome to the Direct4Ag service"}
