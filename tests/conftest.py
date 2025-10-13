"""Test configuration and fixtures."""

import pytest

from py_dmmjp import DMMClient


@pytest.fixture
def mock_api_key() -> str:
    """Provide a mock API key for testing."""
    return "test_api_key_12345"


@pytest.fixture
def mock_affiliate_key() -> str:
    """Provide a mock affiliate key for testing."""
    return "test_affiliate_key_67890"


# pylint: disable=redefined-outer-name
@pytest.fixture
def dmm_client(mock_api_key: str, mock_affiliate_key: str) -> DMMClient:
    """Provide a DMMClient instance for testing."""
    return DMMClient(api_key=mock_api_key, affiliate_id=mock_affiliate_key)


@pytest.fixture
def mock_response_data() -> dict:
    """Provide mock response data from DMM API."""
    return {
        "result": {
            "total_count": 100,
            "items": [
                {
                    "content_id": "test123",
                    "title": "Test Product",
                    "comment": "Test description",
                    "prices": {"price": 1000},
                    "imageURL": {"large": "https://example.com/image.jpg"},
                    "floor_name": "digital",
                    "genre": ["action", "adventure"],
                },
                {
                    "content_id": "test456",
                    "title": "Another Product",
                    "comment": "Another description",
                    "prices": {"price": 2000},
                    "imageURL": {"large": "https://example.com/image2.jpg"},
                    "floor_name": "digital",
                    "genre": ["romance"],
                },
            ],
        }
    }
