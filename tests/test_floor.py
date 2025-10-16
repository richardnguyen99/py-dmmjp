"""
Test floor, service, and site data models with actual implementation.
"""

from typing import Any, Dict

import pytest

from py_dmmjp.floor import Floor, Service, Site
from tests.floor_test_base import FloorTestBase, ServiceTestBase, SiteTestBase


class TestFloorWithRealData(FloorTestBase):
    """Test floor with real API response data."""

    @pytest.fixture
    def floor_data(self) -> Dict[str, Any]:
        return {"id": "1", "name": "AKB48", "code": "akb48"}

    def test_floor_basic_fields(self, floor_data: Dict[str, Any]) -> None:
        floor = Floor.from_dict(floor_data)

        assert floor.id == "1"
        assert floor.name == "AKB48"
        assert floor.code == "akb48"

    def test_floor_from_dict(self, floor_data: Dict[str, Any]) -> None:
        floor = Floor.from_dict(floor_data)

        assert isinstance(floor, Floor)
        assert floor.id == floor_data["id"]
        assert floor.name == floor_data["name"]
        assert floor.code == floor_data["code"]

    def test_floor_id_type(self, floor_data: Dict[str, Any]) -> None:
        floor = Floor.from_dict(floor_data)

        assert isinstance(floor.id, str)

    def test_floor_name_validation(self, floor_data: Dict[str, Any]) -> None:
        floor = Floor.from_dict(floor_data)

        assert floor.name is not None
        assert len(floor.name) > 0
        assert isinstance(floor.name, str)

    def test_floor_code_validation(self, floor_data: Dict[str, Any]) -> None:
        floor = Floor.from_dict(floor_data)

        assert floor.code is not None
        assert len(floor.code) > 0
        assert isinstance(floor.code, str)

    def test_floor_empty_data_handling(self, floor_data: Dict[str, Any]) -> None:
        empty_data: Dict[str, Any] = {}
        floor = Floor.from_dict(empty_data)

        assert floor.id == ""
        assert floor.name == ""
        assert floor.code == ""

    def test_floor_default_values(self, floor_data: Dict[str, Any]) -> None:
        partial_data: Dict[str, Any] = {"id": "1"}
        floor = Floor.from_dict(partial_data)

        assert floor.id == "1"
        assert floor.name == ""
        assert floor.code == ""


class TestServiceWithRealData(ServiceTestBase):
    """Test service with real API response data."""

    @pytest.fixture
    def service_data(self) -> Dict[str, Any]:
        return {
            "name": "AKB48グループ",
            "code": "lod",
            "floor": [
                {"id": "1", "name": "AKB48", "code": "akb48"},
                {"id": "2", "name": "SKE48", "code": "ske48"},
                {"id": "3", "name": "NMB48", "code": "nmb48"},
            ],
        }

    def test_service_basic_fields(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert service.name == "AKB48グループ"
        assert service.code == "lod"

    def test_service_floors_list(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert isinstance(service.floors, list)
        assert len(service.floors) == 3

    def test_service_from_dict(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert isinstance(service, Service)
        assert service.name == service_data["name"]
        assert service.code == service_data["code"]
        assert len(service.floors) == len(service_data["floor"])

    def test_service_nested_floors(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        for floor in service.floors:
            assert isinstance(floor, Floor)
            assert floor.id is not None
            assert floor.name is not None
            assert floor.code is not None

    def test_service_empty_floors(self, service_data: Dict[str, Any]) -> None:
        empty_service_data: Dict[str, Any] = {
            "name": "Test",
            "code": "test",
            "floor": [],
        }
        service = Service.from_dict(empty_service_data)

        assert isinstance(service.floors, list)
        assert len(service.floors) == 0

    def test_service_multiple_floors(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert len(service.floors) == 3
        assert service.floors[0].code == "akb48"
        assert service.floors[1].code == "ske48"
        assert service.floors[2].code == "nmb48"

    def test_service_name_validation(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert service.name is not None
        assert len(service.name) > 0
        assert isinstance(service.name, str)

    def test_service_code_validation(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert service.code is not None
        assert len(service.code) > 0
        assert isinstance(service.code, str)

    def test_service_floors_type(self, service_data: Dict[str, Any]) -> None:
        service = Service.from_dict(service_data)

        assert isinstance(service.floors, list)
        for floor in service.floors:
            assert isinstance(floor, Floor)

    def test_service_default_values(self, service_data: Dict[str, Any]) -> None:
        partial_data: Dict[str, Any] = {"name": "Test"}
        service = Service.from_dict(partial_data)

        assert service.name == "Test"
        assert service.code == ""
        assert isinstance(service.floors, list)
        assert len(service.floors) == 0


class TestSiteWithRealData(SiteTestBase):
    """Test site with real API response data."""

    @pytest.fixture
    def site_data(self) -> Dict[str, Any]:
        return {
            "name": "DMM.com（一般）",
            "code": "DMM.com",
            "service": [
                {
                    "name": "AKB48グループ",
                    "code": "lod",
                    "floor": [
                        {"id": "1", "name": "AKB48", "code": "akb48"},
                        {"id": "2", "name": "SKE48", "code": "ske48"},
                    ],
                },
                {
                    "name": "DMMブックス",
                    "code": "ebook",
                    "floor": [
                        {"id": "19", "name": "コミック", "code": "comic"},
                        {"id": "20", "name": "写真集", "code": "photo"},
                    ],
                },
            ],
        }

    def test_site_basic_fields(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert site.name == "DMM.com（一般）"
        assert site.code == "DMM.com"

    def test_site_services_list(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert isinstance(site.services, list)
        assert len(site.services) == 2

    def test_site_from_dict(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert isinstance(site, Site)
        assert site.name == site_data["name"]
        assert site.code == site_data["code"]
        assert len(site.services) == len(site_data["service"])

    def test_site_nested_services(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        for service in site.services:
            assert isinstance(service, Service)
            assert service.name is not None
            assert service.code is not None

    def test_site_nested_floors(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        for service in site.services:
            for floor in service.floors:
                assert isinstance(floor, Floor)
                assert floor.id is not None
                assert floor.name is not None
                assert floor.code is not None

    def test_site_empty_services(self, site_data: Dict[str, Any]) -> None:
        empty_site_data: Dict[str, Any] = {
            "name": "Test",
            "code": "test",
            "service": [],
        }
        site = Site.from_dict(empty_site_data)

        assert isinstance(site.services, list)
        assert len(site.services) == 0

    def test_site_multiple_services(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert len(site.services) == 2
        assert site.services[0].code == "lod"
        assert site.services[1].code == "ebook"

    def test_site_name_validation(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert site.name is not None
        assert len(site.name) > 0
        assert isinstance(site.name, str)

    def test_site_code_validation(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert site.code is not None
        assert len(site.code) > 0
        assert isinstance(site.code, str)

    def test_site_services_type(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert isinstance(site.services, list)
        for service in site.services:
            assert isinstance(service, Service)

    def test_site_default_values(self, site_data: Dict[str, Any]) -> None:
        partial_data: Dict[str, Any] = {"name": "Test"}
        site = Site.from_dict(partial_data)

        assert site.name == "Test"
        assert site.code == ""
        assert isinstance(site.services, list)
        assert len(site.services) == 0

    def test_site_hierarchy(self, site_data: Dict[str, Any]) -> None:
        site = Site.from_dict(site_data)

        assert isinstance(site, Site)
        assert len(site.services) == 2
        assert len(site.services[0].floors) == 2
        assert len(site.services[1].floors) == 2
        assert site.services[0].floors[0].code == "akb48"
        assert site.services[1].floors[0].code == "comic"
