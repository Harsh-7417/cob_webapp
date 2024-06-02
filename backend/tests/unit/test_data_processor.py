import json
import os
import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from fastapi import status

from src.data_processor import COBDataExtractor, COBDataTransformer

mock_file_path = os.path.join(os.path.dirname(__file__), "mock_data", "cob_api_response.json")

with open(mock_file_path, "r", encoding="utf-8") as file:
    mock_cob_api_response = json.load(file)


class TestCOBDataExtractor(unittest.TestCase):
    """Test case(s) for all scenario's related to data extraction from ECB-COB endpoint"""

    def setUp(self):
        self.extractor = COBDataExtractor()

    @patch("src.data_processor.requests.get")
    def test_extract_data_200_status_code(self, mock_get):
        """Test successful data extraction with a 200 OK status code."""
        mock_response = Mock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = mock_cob_api_response
        mock_response.headers.get.return_value = "Fri, 31 May 2024 21:28:00 GMT"
        mock_get.return_value = mock_response

        result = self.extractor.extract_data()

        self.assertEqual(result, mock_cob_api_response)
        self.assertEqual(self.extractor.last_modified, "Fri, 31 May 2024 21:28:00 GMT")

    @patch("src.data_processor.requests.get")
    def test_extract_data_304_status_code(self, mock_get):
        """Test data extraction with a 304 Not Modified status code."""
        mock_response = Mock()
        mock_response.status_code = status.HTTP_304_NOT_MODIFIED
        mock_get.return_value = mock_response

        result = self.extractor.extract_data()

        self.assertEqual(result, {})
        self.assertEqual(self.extractor.last_modified, "Fri, 31 May 2024 21:28:00 GMT")

    @patch("src.data_processor.requests.get")
    def test_extract_data_exception(self, mock_get):
        """Test handling of exceptions during data extraction"""
        mock_get.side_effect = Exception("Test exception")
        result = self.extractor.extract_data()
        self.assertEqual(result, {})
        self.assertEqual(self.extractor.last_modified, "Fri, 31 May 2024 21:28:00 GMT")


class TestCOBDataTransformer(unittest.TestCase):
    """Test case(s) for all scenario's related to raw data transformation to DB compatible format"""

    def test_transform_data(self):
        """Test data transformation logic."""

        expected_data = [
            {
                "id": 202402,
                "start_date": datetime(2024, 2, 1).date(),
                "end_date": datetime(2024, 2, 29).date(),
                "value": 2.68,
            },
            {
                "id": 202403,
                "start_date": datetime(2024, 3, 1).date(),
                "end_date": datetime(2024, 3, 31).date(),
                "value": 3.11,
            },
        ]

        transformed_data = COBDataTransformer.transform_data(mock_cob_api_response)
        self.assertEqual(transformed_data, expected_data)
        self.assertIsNotNone(COBDataExtractor.last_modified)

    def test_transform_data_exception(self):
        """Test handling of exceptions during data transformation."""
        raw_data = {"food": "pizza"}

        transformed_data = COBDataTransformer.transform_data(raw_data)

        self.assertEqual(transformed_data, [])
        self.assertIsNone(COBDataExtractor.last_modified)
