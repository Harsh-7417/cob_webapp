"""contains Pydantic schema definitions for data validation and serialization."""

from datetime import date

from pydantic import BaseModel


class COBData(BaseModel):
    """Schema for representing COB data."""

    id: int
    start_date: date
    end_date: date
    value: float
