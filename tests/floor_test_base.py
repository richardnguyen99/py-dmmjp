"""
Base classes for floor, service, and site testing with abstract test methods.
"""

from abc import abstractmethod
from typing import Any, Dict

import pytest


class FloorTestBase:
    """Abstract base class for floor tests."""

    @pytest.fixture
    @abstractmethod
    def floor_data(self) -> Dict[str, Any]:
        """Mock floor data - must be implemented by subclasses."""

    @abstractmethod
    def test_floor_basic_fields(self, floor_data: Dict[str, Any]) -> None:
        """Test basic floor fields (id, name, code)."""

    @abstractmethod
    def test_floor_from_dict(self, floor_data: Dict[str, Any]) -> None:
        """Test creating floor from dictionary."""

    @abstractmethod
    def test_floor_id_type(self, floor_data: Dict[str, Any]) -> None:
        """Test floor ID is string type."""

    @abstractmethod
    def test_floor_name_validation(self, floor_data: Dict[str, Any]) -> None:
        """Test floor name validation."""

    @abstractmethod
    def test_floor_code_validation(self, floor_data: Dict[str, Any]) -> None:
        """Test floor code validation."""

    @abstractmethod
    def test_floor_empty_data_handling(self, floor_data: Dict[str, Any]) -> None:
        """Test handling of empty or missing data."""

    @abstractmethod
    def test_floor_default_values(self, floor_data: Dict[str, Any]) -> None:
        """Test default values for missing fields."""


class ServiceTestBase:
    """Abstract base class for service tests."""

    @pytest.fixture
    @abstractmethod
    def service_data(self) -> Dict[str, Any]:
        """Mock service data - must be implemented by subclasses."""

    @abstractmethod
    def test_service_basic_fields(self, service_data: Dict[str, Any]) -> None:
        """Test basic service fields (name, code)."""

    @abstractmethod
    def test_service_floors_list(self, service_data: Dict[str, Any]) -> None:
        """Test floors list parsing."""

    @abstractmethod
    def test_service_from_dict(self, service_data: Dict[str, Any]) -> None:
        """Test creating service from dictionary."""

    @abstractmethod
    def test_service_nested_floors(self, service_data: Dict[str, Any]) -> None:
        """Test nested floor objects."""

    @abstractmethod
    def test_service_empty_floors(self, service_data: Dict[str, Any]) -> None:
        """Test service with empty floors list."""

    @abstractmethod
    def test_service_multiple_floors(self, service_data: Dict[str, Any]) -> None:
        """Test service with multiple floors."""

    @abstractmethod
    def test_service_name_validation(self, service_data: Dict[str, Any]) -> None:
        """Test service name validation."""

    @abstractmethod
    def test_service_code_validation(self, service_data: Dict[str, Any]) -> None:
        """Test service code validation."""

    @abstractmethod
    def test_service_floors_type(self, service_data: Dict[str, Any]) -> None:
        """Test floors field type is list."""

    @abstractmethod
    def test_service_default_values(self, service_data: Dict[str, Any]) -> None:
        """Test default values for missing fields."""


class SiteTestBase:
    """Abstract base class for site tests."""

    @pytest.fixture
    @abstractmethod
    def site_data(self) -> Dict[str, Any]:
        """Mock site data - must be implemented by subclasses."""

    @abstractmethod
    def test_site_basic_fields(self, site_data: Dict[str, Any]) -> None:
        """Test basic site fields (name, code)."""

    @abstractmethod
    def test_site_services_list(self, site_data: Dict[str, Any]) -> None:
        """Test services list parsing."""

    @abstractmethod
    def test_site_from_dict(self, site_data: Dict[str, Any]) -> None:
        """Test creating site from dictionary."""

    @abstractmethod
    def test_site_nested_services(self, site_data: Dict[str, Any]) -> None:
        """Test nested service objects."""

    @abstractmethod
    def test_site_nested_floors(self, site_data: Dict[str, Any]) -> None:
        """Test nested floor objects within services."""

    @abstractmethod
    def test_site_empty_services(self, site_data: Dict[str, Any]) -> None:
        """Test site with empty services list."""

    @abstractmethod
    def test_site_multiple_services(self, site_data: Dict[str, Any]) -> None:
        """Test site with multiple services."""

    @abstractmethod
    def test_site_name_validation(self, site_data: Dict[str, Any]) -> None:
        """Test site name validation."""

    @abstractmethod
    def test_site_code_validation(self, site_data: Dict[str, Any]) -> None:
        """Test site code validation."""

    @abstractmethod
    def test_site_services_type(self, site_data: Dict[str, Any]) -> None:
        """Test services field type is list."""

    @abstractmethod
    def test_site_default_values(self, site_data: Dict[str, Any]) -> None:
        """Test default values for missing fields."""

    @abstractmethod
    def test_site_hierarchy(self, site_data: Dict[str, Any]) -> None:
        """Test complete site-service-floor hierarchy."""
