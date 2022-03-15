from fastapi import FastAPI
from app.routers import model
from app.routers import item
from app.routers import user

import uvicorn

app = FastAPI()

app.include_router(model.router)
app.include_router(item.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
