"""Entry point of FastAPI backend.Contains FastAPI app configuration and router"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import logger
from src.database import init_db
from src.routes import router

origins = [
    "http://localhost:3000",  # Local development
    "http://frontend:3000",  # Frontend running in Docker
]

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize the database on startup"""
    init_db()
    logger.info("Database succesfully initialised")


app.include_router(router, prefix="/v1")
