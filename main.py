from fastapi import FastAPI
from app.routers.api import router as api_router
from app.routers.webhook import router as webhook_router


app = FastAPI()

app.include_router(api_router)
app.include_router(webhook_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



