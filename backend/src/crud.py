"""contains all crud/database operations required to process a request"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src import logger
from src.data_processor import COBDataExtractor, COBDataTransformer
from src.models import COBData


def get_all_cob_data(db: Session) -> List[COBData]:
    """Retrieve all COB data entries from the database."""
    try:
        result = db.execute(select(COBData).order_by(COBData.id))
        data = result.scalars().all()
        return data
    except Exception as err:
        logger.exception("Error fetching data from DB", err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching data from DB"
        ) from err


def refresh_cob_data(db: Session) -> None:
    """Truncate and load COB data in database"""
    data = COBDataExtractor().extract_data()
    if data:
        transformed_data = COBDataTransformer.transform_data(data)
        table_name = COBData.__tablename__
        try:
            db.execute(text(f"TRUNCATE TABLE {table_name}"))
            db.bulk_insert_mappings(COBData, transformed_data)
            db.commit()
            return None
        except Exception as err:
            db.rollback()
            logger.exception("Error refreshing data", err)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error refreshing data"
            ) from err
