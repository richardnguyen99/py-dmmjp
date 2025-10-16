"""
Base class for actress testing with abstract test methods.
"""

# pylint: disable=too-many-public-methods

from abc import abstractmethod
from typing import Any, Dict

import pytest


class ActressTestBase:
    """Abstract base class for actress tests."""

    @pytest.fixture
    @abstractmethod
    def actress_data(self) -> Dict[str, Any]:
        """Mock actress data - must be implemented by subclasses."""

    @abstractmethod
    def test_actress_basic_fields(self, actress_data: Dict[str, Any]) -> None:
        """Test basic actress fields (id, name, ruby)."""

    @abstractmethod
    def test_actress_measurements(self, actress_data: Dict[str, Any]) -> None:
        """Test measurement fields (bust, waist, hip, height, cup)."""

    @abstractmethod
    def test_actress_personal_info(self, actress_data: Dict[str, Any]) -> None:
        """Test personal information (birthday, blood_type, hobby, prefectures)."""

    @abstractmethod
    def test_actress_image_urls(self, actress_data: Dict[str, Any]) -> None:
        """Test image URL parsing (small and large images)."""

    @abstractmethod
    def test_actress_list_urls(self, actress_data: Dict[str, Any]) -> None:
        """Test list URL parsing (digital, monthly, mono)."""

    @abstractmethod
    def test_actress_from_dict(self, actress_data: Dict[str, Any]) -> None:
        """Test creating actress from dictionary."""

    @abstractmethod
    def test_actress_safe_int_conversion(self, actress_data: Dict[str, Any]) -> None:
        """Test safe integer conversion for measurements."""

    @abstractmethod
    def test_actress_optional_fields(self, actress_data: Dict[str, Any]) -> None:
        """Test handling of optional/null fields."""

    @abstractmethod
    def test_actress_nested_objects(self, actress_data: Dict[str, Any]) -> None:
        """Test nested objects (image_url, list_url)."""

    @abstractmethod
    def test_actress_image_url_from_dict(self, actress_data: Dict[str, Any]) -> None:
        """Test ActressImageURL creation from dictionary."""

    @abstractmethod
    def test_actress_list_url_from_dict(self, actress_data: Dict[str, Any]) -> None:
        """Test ActressListURL creation from dictionary."""

    @abstractmethod
    def test_actress_empty_data_handling(self, actress_data: Dict[str, Any]) -> None:
        """Test handling of empty or missing data."""

    @abstractmethod
    def test_actress_string_measurements(self, actress_data: Dict[str, Any]) -> None:
        """Test conversion of string measurements to integers."""

    @abstractmethod
    def test_actress_invalid_data_handling(self, actress_data: Dict[str, Any]) -> None:
        """Test handling of invalid data types."""

    @abstractmethod
    def test_actress_birthday_format(self, actress_data: Dict[str, Any]) -> None:
        """Test birthday format handling."""

    @abstractmethod
    def test_actress_cup_size_validation(self, actress_data: Dict[str, Any]) -> None:
        """Test cup size field validation."""

    @abstractmethod
    def test_actress_prefecture_data(self, actress_data: Dict[str, Any]) -> None:
        """Test prefecture/birthplace data."""

    @abstractmethod
    def test_actress_hobby_data(self, actress_data: Dict[str, Any]) -> None:
        """Test hobby/interests data."""

    @abstractmethod
    def test_actress_blood_type_data(self, actress_data: Dict[str, Any]) -> None:
        """Test blood type data."""

    @abstractmethod
    def test_actress_url_formatting(self, actress_data: Dict[str, Any]) -> None:
        """Test URL formatting in image and list URLs."""
