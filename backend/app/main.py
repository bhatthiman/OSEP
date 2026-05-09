from fastapi import FastAPI

from app.api.router import api_router

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

app = FastAPI(
    title="OSEP Platform",
    description="Open Static Equipment Platform by MechXcel OSS",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUTS_DIR = BASE_DIR / "outputs"

app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUTS_DIR),
    name="outputs"
)



app.include_router(api_router)

@app.get("/")
def root():
    return {
        "platform": "OSEP",
        "organization": "MechXcel OSS",
        "status": "running"
    }
