"""
Integration tests for DMM client with real API requests.
"""

# pylint: disable=redefined-outer-name,import-outside-toplevel


import os

import pytest

from py_dmmjp.client import DMMClient
from py_dmmjp.exceptions import DMMAuthError
from py_dmmjp.product import Product


def get_env_or_skip(var_name: str) -> str:
    """Get environment variable or skip test if not found."""

    value = os.getenv(var_name)
    if not value:
        pytest.skip(f"Environment variable {var_name} not set")
    return value


@pytest.fixture
def dmm_client() -> DMMClient:
    """Create DMM client using environment variables."""

    api_key = get_env_or_skip("APP_ID")
    affiliate_id = get_env_or_skip("AFF_ID")

    return DMMClient(api_key=api_key, affiliate_id=affiliate_id)


@pytest.mark.integration
class TestDMMClientIntegration:
    """Integration tests for DMM client with real API calls."""

    def test_client_authentication(self, dmm_client):
        """Test that client can authenticate with valid credentials."""

        assert dmm_client.app_id is not None
        assert dmm_client.affiliate_id is not None

    def test_get_products_basic_request(self, dmm_client):
        """Test basic product retrieval from FANZA."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=5
        )

        assert isinstance(products, list)
        assert len(products) <= 5

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code == "digital"
            assert product.floor_code == "videoa"
            assert product.title is not None
            assert product.content_id is not None

    def test_get_products_with_keyword_search(self, dmm_client):
        """Test product search with keyword."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", keyword="S1", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code == "digital"

    def test_get_products_dmm_com_site(self, dmm_client):
        """Test product retrieval from DMM.com (general content)."""

        products = dmm_client.get_products(
            site="DMM.com", service="mono", floor="book", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code == "mono"
            assert product.floor_code == "book"

    def test_get_products_with_sorting(self, dmm_client):
        """Test product retrieval with different sort options."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", sort="date", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.date is not None

    def test_get_products_ebook_service(self, dmm_client):
        """Test ebook product retrieval."""

        products = dmm_client.get_products(
            site="FANZA", service="ebook", floor="comic", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code == "ebook"
            assert product.floor_code == "comic"

    def test_product_data_completeness(self, dmm_client):
        """Test that product data contains expected fields."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.service_code is not None
        assert product.service_name is not None
        assert product.floor_code is not None
        assert product.floor_name is not None
        assert product.category_name is not None
        assert product.content_id is not None
        assert product.product_id is not None
        assert product.title is not None
        assert product.url is not None
        assert product.affiliate_url is not None
        assert product.image_url is not None
        assert product.prices is not None

    def test_product_item_info_data(self, dmm_client):
        """Test that product item info contains valid data."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.item_info is not None
        assert isinstance(product.genres, list)
        assert isinstance(product.actresses, list)
        assert isinstance(product.makers, list)
        assert isinstance(product.series, list)

    def test_product_pricing_data(self, dmm_client):
        """Test product pricing information."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.prices is not None
        assert product.current_price is not None
        assert isinstance(product.current_price, int)
        assert product.current_price > 0

    def test_product_image_urls(self, dmm_client):
        """Test product image URL data."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.image_url is not None
        assert product.image_url.list is not None
        assert product.image_url.list.startswith("http")

    def test_product_review_data(self, dmm_client):
        """Test product review information."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", sort="review", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        if product.review is not None:
            assert product.review_count >= 0
            assert product.review_average is None or product.review_average >= 0

    def test_product_sample_data(self, dmm_client):
        """Test product sample images and videos."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert isinstance(product.sample_images, list)
        assert isinstance(product.sample_images_large, list)

    def test_error_handling_invalid_service(self, dmm_client):
        """Test error handling with invalid service."""

        from py_dmmjp.exceptions import DMMAPIError

        with pytest.raises(DMMAPIError) as exc_info:
            dmm_client.get_products(
                site="FANZA", service="invalid_service", floor="videoa", hits=1
            )

        # Verify that the error contains information about the invalid service
        assert "400" in str(exc_info.value)
        assert "BAD REQUEST" in str(exc_info.value) or "Invalid Request Error" in str(
            exc_info.value
        )

    def test_empty_results_valid_request(self, dmm_client):
        """Test handling of valid requests that return no results."""

        # Use a very specific keyword that's unlikely to match any products
        products = dmm_client.get_products(
            site="FANZA",
            service="digital",
            floor="videoa",
            keyword="xyznomatchkeyword12345",
            hits=1,
        )

        assert isinstance(products, list)
        assert len(products) == 0

    def test_error_handling_invalid_floor(self, dmm_client):
        """Test error handling with invalid floor for a valid service."""

        from py_dmmjp.exceptions import DMMAPIError

        with pytest.raises(DMMAPIError) as exc_info:
            dmm_client.get_products(
                site="FANZA", service="digital", floor="invalid_floor", hits=1
            )

        assert "400" in str(exc_info.value)

    def test_error_handling_invalid_site(self, dmm_client):
        """Test error handling with invalid site parameter."""

        from py_dmmjp.exceptions import DMMAPIError

        with pytest.raises(DMMAPIError) as exc_info:
            dmm_client.get_products(
                site="INVALID_SITE", service="digital", floor="videoa", hits=1
            )

        assert "400" in str(exc_info.value)

    def test_pagination_with_offset(self, dmm_client):
        """Test pagination using offset parameter."""

        first_page = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=2, offset=1
        )

        second_page = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=2, offset=3
        )

        assert len(first_page) <= 2
        assert len(second_page) <= 2

        if len(first_page) > 0 and len(second_page) > 0:
            assert first_page[0].content_id != second_page[0].content_id

    def test_client_context_manager(self):
        """Test client as context manager."""

        api_key = get_env_or_skip("APP_ID")
        affiliate_id = get_env_or_skip("AFF_ID")

        with DMMClient(api_key=api_key, affiliate_id=affiliate_id) as client:
            products = client.get_products(
                site="FANZA", service="digital", floor="videoa", hits=1
            )

            assert isinstance(products, list)

    def test_raw_data_access(self, dmm_client):
        """Test access to raw API response data."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.raw_data is not None
        assert isinstance(product.raw_data, dict)
        assert "service_code" in product.raw_data
        assert "content_id" in product.raw_data

    def test_product_to_dict_conversion(self, dmm_client):
        """Test product to dictionary conversion."""

        products = dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        product_dict = product.to_dict()

        assert isinstance(product_dict, dict)
        assert product_dict["service_code"] == product.service_code
        assert product_dict["content_id"] == product.content_id
        assert product_dict["title"] == product.title


@pytest.mark.integration
class TestDMMClientAuthenticationErrors:
    """Test authentication error scenarios."""

    def test_invalid_api_key(self):
        """Test client with invalid API key."""

        with pytest.raises(DMMAuthError):
            DMMClient(api_key="", affiliate_id="valid_id")

    def test_invalid_affiliate_id(self):
        """Test client with invalid affiliate ID."""

        with pytest.raises(DMMAuthError):
            DMMClient(api_key="valid_key", affiliate_id="")

    def test_both_invalid_credentials(self):
        """Test client with both invalid credentials."""

        with pytest.raises(DMMAuthError):
            DMMClient(api_key="", affiliate_id="")


@pytest.mark.integration
class TestDMMClientEnvironmentVariables:
    """Test environment variable handling."""

    def test_env_file_support(
        self,
    ):
        """Test loading credentials from .env file."""

        # pylint: disable=import-outside-toplevel

        try:
            from dotenv import load_dotenv
        except ImportError:
            pytest.skip("python-dotenv not installed")

        original_dir = os.getcwd()
        try:
            load_dotenv()

            app_id = os.getenv("APP_ID")
            aff_id = os.getenv("AFF_ID")

            assert app_id is not None
            assert aff_id is not None

        finally:
            os.chdir(original_dir)

    def test_environment_variable_precedence(self):
        """Test that environment variables are properly loaded."""

        app_id = os.getenv("APP_ID")
        aff_id = os.getenv("AFF_ID")

        if app_id and aff_id:
            client = DMMClient(api_key=app_id, affiliate_id=aff_id)
            assert client.app_id == app_id
            assert client.affiliate_id == aff_id
        else:
            pytest.skip("Environment variables APP_ID and AFF_ID not set")
