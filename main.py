from fastapi import FastAPI
from profile.routers_profile import router as profile_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Tarot"}

@app.get("/api")
def read_root():
    return {"api root": "not for web access"}

app.include_router(profile_router, prefix="/api")