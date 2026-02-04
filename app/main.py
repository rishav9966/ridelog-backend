from fastapi import FastAPI
from app.core.config import settings
from app.api.users import router as user_router
from app.api.rides import router as ride_router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(user_router)
app.include_router(ride_router)


@app.get("/")
def health():
    return {"status": "ok"}
