"""contains the definition of SQLAlchemy models representing database tables."""

from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class COBData(Base):
    """Table structure for COB data"""

    __tablename__ = "cob_data"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    value = Column(Float)
