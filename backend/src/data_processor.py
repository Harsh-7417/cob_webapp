"""Data pipeline to fetch and transform data from COB API"""

import os
from typing import Dict, List

import requests
from dateutil import parser
from fastapi import status

from src import logger
from src.models import COBData


class COBDataExtractor:
    """Fetch data from COB api endpoint."""

    last_modified = None  # if we have a requirement that may need mutihreading or concurrency then we can transform it to singleton pattern

    def __init__(self):
        self.url = os.getenv("COB_API")
        self.headers = {"Accept": "application/json"}

    def extract_data(self) -> Dict:
        """Send request to COB endpoint and read if data has been changed."""
        if COBDataExtractor.last_modified:
            self.headers["If-Modified-Since"] = COBDataExtractor.last_modified
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            if response.status_code == status.HTTP_304_NOT_MODIFIED:
                logger.debug(
                    f"Data Unchanged since {COBDataExtractor.last_modified}, received status code 304"
                )
                return {}
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            COBDataExtractor.last_modified = response.headers.get("Last-Modified")
            logger.debug("Data fetched succesfully from COB api, received status code 200")
            return response.json()
        except Exception:
            logger.exception("Error fetching data from COB api")
            return {}


class COBDataTransformer:
    """Utility class to transform raw data from COB. We can extend it if we want to add specific tranformation logic to raw data"""

    @staticmethod
    def transform_data(data: Dict) -> List[COBData]:
        """Transformation logic to convert COB raw data to DB compatible format"""
        try:
            observations = data["dataSets"][0]["series"]["0:0:0:0:0:0:0:0:0:0"]["observations"]
            structure = data["structure"]["dimensions"]["observation"][0]["values"]

            transformed_data = []
            for idx, value in observations.items():
                observation = structure[int(idx)]
                transformed_item: COBData = {
                    "id": int(observation["id"].replace("-", "")),
                    "start_date": parser.parse(observation["start"]).date(),
                    "end_date": parser.parse(observation["end"]).date(),
                    "value": value[0],
                }
                transformed_data.append(transformed_item)

            return transformed_data
        except Exception:
            logger.exception("Error transforming raw COB data")
            return []
