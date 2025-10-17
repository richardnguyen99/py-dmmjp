"""
Base classes for genre testing with abstract test methods.
"""

from abc import abstractmethod
from typing import Any, Dict

import pytest


class GenreTestBase:
    """Abstract base class for genre tests."""

    @pytest.fixture
    @abstractmethod
    def genre_data(self) -> Dict[str, Any]:
        """Mock genre data - must be implemented by subclasses."""

    @abstractmethod
    def test_genre_basic_fields(self, genre_data: Dict[str, Any]) -> None:
        """Test basic genre fields (genre_id, name, ruby, list_url)."""

    @abstractmethod
    def test_genre_from_dict(self, genre_data: Dict[str, Any]) -> None:
        """Test creating genre from dictionary."""

    @abstractmethod
    def test_genre_id_type(self, genre_data: Dict[str, Any]) -> None:
        """Test genre ID is string type."""

    @abstractmethod
    def test_genre_name_validation(self, genre_data: Dict[str, Any]) -> None:
        """Test genre name validation."""

    @abstractmethod
    def test_genre_ruby_validation(self, genre_data: Dict[str, Any]) -> None:
        """Test genre ruby (phonetic) validation."""

    @abstractmethod
    def test_genre_list_url_validation(self, genre_data: Dict[str, Any]) -> None:
        """Test genre list URL validation."""

    @abstractmethod
    def test_genre_empty_data_handling(self, genre_data: Dict[str, Any]) -> None:
        """Test handling of empty or missing data."""

    @abstractmethod
    def test_genre_default_values(self, genre_data: Dict[str, Any]) -> None:
        """Test default values for missing fields."""
