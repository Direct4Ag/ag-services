from fastapi import FastAPI
from routers import model
from routers import item
from routers import user

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