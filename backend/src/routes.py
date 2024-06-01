"""contains FastAPI route definitions for handling HTTP requests."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.crud import get_all_cob_data, refresh_cob_data
from src.database import get_db_session
from src.schemas import COBData

router = APIRouter()


@router.get("/data", response_model=List[COBData])
def get_cob_data(db: Session = Depends(get_db_session)):
    """Endpoint for retrieving COB data."""
    return get_all_cob_data(db)


@router.post("/refresh-data", status_code=status.HTTP_204_NO_CONTENT)
def refresh_data(db: Session = Depends(get_db_session)):
    """Endpoint for refreshing COB data."""
    refresh_cob_data(db)


@router.get("/health-check")
def health_check():
    """Endpoint to check if Backend is up and running. As of now it is dummy but we can redefine as per requirement"""
    return "ok"
