"""
Integration tests for AsyncDMMClient with real API requests for product-related functionality.
"""

# pylint: disable=R0904,W0212,R0915

import sys

import pytest

if sys.version_info < (3, 9):
    pytest.skip("AsyncDMMClient requires Python 3.9+", allow_module_level=True)

import asyncio

import pytest_asyncio

from py_dmmjp.async_client import AsyncDMMClient
from py_dmmjp.exceptions import DMMAPIError
from py_dmmjp.product import Product


@pytest.mark.integration
@pytest.mark.asyncio(loop_scope="module")
class TestAsyncDMMClientWithProductIntegration:
    """Integration tests for async DMM client with real API calls for products."""

    @pytest_asyncio.fixture(loop_scope="module")
    async def async_dmm_client(self, app_id: str, aff_id: str):
        """Create an async DMM client for testing."""

        async with AsyncDMMClient(api_key=app_id, affiliate_id=aff_id) as client:
            yield client

    async def test_client_authentication(
        self, async_dmm_client: AsyncDMMClient
    ) -> None:
        """Test that async client can authenticate with valid credentials."""

        assert async_dmm_client.app_id is not None
        assert async_dmm_client.affiliate_id is not None

    async def test_get_products_basic_request(
        self, async_dmm_client: AsyncDMMClient
    ) -> None:
        """Test basic product retrieval from FANZA."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=5
        )

        assert isinstance(products, list)
        assert len(products) <= 5

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code is not None
            assert product.content_id is not None
            assert product.title is not None

    async def test_get_products_with_keyword_search(self, async_dmm_client):
        """Test product search with keyword."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", keyword="S1", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.content_id is not None

    async def test_get_products_dmm_com_site(self, async_dmm_client):
        """Test product retrieval from DMM.com (general content)."""

        products = await async_dmm_client.get_products(
            site="DMM.com", service="mono", floor="book", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code == "mono"

    async def test_get_products_with_sorting(self, async_dmm_client):
        """Test product retrieval with different sort options."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", sort="date", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)

    async def test_get_products_ebook_service(self, async_dmm_client):
        """Test ebook product retrieval."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="ebook", floor="comic", hits=3
        )

        assert isinstance(products, list)
        assert len(products) <= 3

        for product in products:
            assert isinstance(product, Product)
            assert product.service_code == "ebook"

    async def test_product_data_completeness(self, async_dmm_client):
        """Test that product data contains expected fields."""

        products = await async_dmm_client.get_products(
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

    async def test_product_item_info_data(self, async_dmm_client):
        """Test that product item info contains valid data."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.item_info is not None
        assert isinstance(product.genres, list)
        assert isinstance(product.actresses, list)
        assert isinstance(product.makers, list)
        assert isinstance(product.series, list)

    async def test_product_pricing_data(self, async_dmm_client):
        """Test product pricing information."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.prices is not None
        assert product.current_price is not None
        assert isinstance(product.current_price, int)
        assert product.current_price > 0

    async def test_product_image_urls(self, async_dmm_client):
        """Test product image URL data."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.image_url is not None
        assert product.image_url.list is not None
        assert product.image_url.list.startswith("http")

    async def test_product_review_data(self, async_dmm_client):
        """Test product review information."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", sort="review", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        if product.review is not None:
            assert product.review.count >= 0
            assert product.review.average >= 0

    async def test_product_sample_data(self, async_dmm_client):
        """Test product sample images and videos."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert isinstance(product.sample_images, list)
        assert isinstance(product.sample_images_large, list)

    async def test_error_handling_invalid_service(self, async_dmm_client):
        """Test error handling with invalid service."""

        with pytest.raises(DMMAPIError) as exc_info:
            await async_dmm_client.get_products(
                site="FANZA", service="invalid_service", floor="videoa", hits=1
            )

        assert "400" in str(exc_info.value)
        assert "BAD REQUEST" in str(exc_info.value) or "Invalid Request Error" in str(
            exc_info.value
        )

    async def test_empty_results_valid_request(self, async_dmm_client):
        """Test handling of valid requests that return no results."""

        products = await async_dmm_client.get_products(
            site="FANZA",
            service="digital",
            floor="videoa",
            keyword="xyznomatchkeyword12345",
            hits=1,
        )

        assert isinstance(products, list)
        assert len(products) == 0

    async def test_error_handling_invalid_floor(self, async_dmm_client):
        """Test error handling with invalid floor for a valid service."""

        with pytest.raises(DMMAPIError) as exc_info:
            await async_dmm_client.get_products(
                site="FANZA", service="digital", floor="invalid_floor", hits=1
            )

        assert "400" in str(exc_info.value)

    async def test_error_handling_invalid_site(self, async_dmm_client):
        """Test error handling with invalid site parameter."""

        with pytest.raises(DMMAPIError) as exc_info:
            await async_dmm_client.get_products(
                site="InvalidSite", service="digital", floor="videoa", hits=1
            )

        assert "400" in str(exc_info.value)

    async def test_pagination_with_offset(self, async_dmm_client):
        """Test pagination using offset parameter."""

        first_page = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=2, offset=1
        )

        second_page = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=2, offset=3
        )

        assert len(first_page) <= 2
        assert len(second_page) <= 2

        if len(first_page) > 0 and len(second_page) > 0:
            assert first_page[0].content_id != second_page[0].content_id

    async def test_client_context_manager(self, app_id, aff_id):
        """Test async client as context manager."""

        async with AsyncDMMClient(api_key=app_id, affiliate_id=aff_id) as client:
            products = await client.get_products(
                site="FANZA", service="digital", floor="videoa", hits=1
            )
            assert len(products) >= 0

    async def test_raw_data_access(self, async_dmm_client):
        """Test access to raw API response data."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        assert product.raw_data is not None
        assert isinstance(product.raw_data, dict)
        assert "service_code" in product.raw_data
        assert "content_id" in product.raw_data

    async def test_product_to_dict_conversion(self, async_dmm_client):
        """Test product to dictionary conversion."""

        products = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products) >= 1
        product = products[0]

        product_dict = product.to_dict()

        assert isinstance(product_dict, dict)
        assert product_dict["service_code"] == product.service_code
        assert product_dict["content_id"] == product.content_id
        assert product_dict["title"] == product.title

    async def test_product_with_fanza_cid(self, async_dmm_client):
        """Test retrieving a single product by content ID (CID)."""

        cid = "mird00127"
        product = await async_dmm_client.get_product_by_cid(cid, site="FANZA")

        assert product is not None
        assert isinstance(product, Product)

        assert product.service_code == "digital"
        assert product.service_name == "動画"
        assert product.floor_code == "videoa"
        assert product.floor_name == "ビデオ"
        assert product.category_name == "ビデオ (動画)"
        assert product.content_id == cid
        assert product.product_id == cid
        assert product.title is not None
        assert "国民的アイドルM-girls" in product.title
        assert product.volume == 237

        assert product.review is not None
        assert product.review.count == 10
        assert product.review.average == 3.4
        assert product.review_count == 10
        assert product.review_average == 3.4

        assert product.url is not None
        assert product.affiliate_url is not None
        assert "mird00127" in product.url

        assert product.image_url is not None
        assert product.image_url.list is not None
        assert product.image_url.small is not None
        assert product.image_url.large is not None
        assert "mird00127pt.jpg" in product.image_url.list

        assert product.sample_image_url is not None
        assert len(product.sample_images) == 10
        assert len(product.sample_images_large) == 10
        assert all("mird00127-" in img for img in product.sample_images)
        assert all("mird00127jp-" in img for img in product.sample_images_large)

        assert product.sample_movie_url is not None
        assert product.sample_movie_url.size_476_306 is not None
        assert product.sample_movie_url.size_560_360 is not None
        assert product.sample_movie_url.size_644_414 is not None
        assert product.sample_movie_url.size_720_480 is not None
        assert product.sample_movie_url.pc_flag == 1
        assert product.sample_movie_url.sp_flag == 1

        assert product.prices is not None
        assert product.prices.price == "300~"
        assert product.prices.list_price == "300~"
        assert len(product.prices.deliveries) == 5
        assert product.current_price == 300
        assert product.original_price == 300

        delivery_types = [d.type for d in product.prices.deliveries]
        assert "stream" in delivery_types
        assert "download" in delivery_types
        assert "hd" in delivery_types
        assert "iosdl" in delivery_types
        assert "androiddl" in delivery_types

        assert product.date is not None
        assert product.date.year == 2013
        assert product.date.month == 11
        assert product.date.day == 28

        assert product.item_info is not None
        assert len(product.genres) == 8
        assert len(product.series) == 1
        assert len(product.makers) == 1
        assert len(product.actresses) == 9
        assert len(product.directors) == 1
        assert len(product.labels) == 1

        genre_names = [g.name for g in product.genres]
        assert "アイドル・芸能人" in genre_names
        assert "乱交" in genre_names
        assert "美少女" in genre_names

        assert product.series[0].name == "国民的アイドルM-girls"
        assert product.makers[0].name == "ムーディーズ"
        assert product.directors[0].name == "ZAMPA"
        assert product.labels[0].name == "MOODYZ REAL"

        actress_names = [a.name for a in product.actresses]
        assert "乙葉ななせ" in actress_names
        assert "鈴村みゆう" in actress_names

        assert product.raw_data is not None
        assert isinstance(product.raw_data, dict)
        assert product.raw_data["content_id"] == cid

    async def test_product_with_mono_cid(self, async_dmm_client):
        """Test retrieving a single product by content ID (CID) from MONO service."""

        cid = "118abp477"
        product = await async_dmm_client.get_product_by_cid(cid, site="FANZA")

        assert product is not None
        assert isinstance(product, Product)

        assert product.service_code == "mono"
        assert product.service_name == "通販"
        assert product.floor_code == "dvd"
        assert product.floor_name == "DVD"
        assert product.category_name == "DVD通販"
        assert product.content_id == cid
        assert product.product_id == cid
        assert product.title == "エンドレスセックス AIKA"
        assert product.volume == 140

        assert product.review is not None
        assert product.review.count == 32
        assert product.review.average == 4.41
        assert product.review_count == 32
        assert product.review_average == 4.41

        assert product.url is not None
        assert product.affiliate_url is not None
        assert "118abp477" in product.url

        assert product.image_url is not None
        assert product.image_url.list is not None
        assert "118abp477pt.jpg" in product.image_url.list

        assert product.sample_image_url is not None
        assert len(product.sample_images) == 13
        assert all("118abp477-" in img for img in product.sample_images)

        assert product.prices is not None
        assert product.prices.price == "2589"
        assert product.prices.list_price == "3278"
        assert product.current_price == 2589
        assert product.original_price == 3278

        assert product.date is not None
        assert product.date.year == 2016
        assert product.date.month == 5
        assert product.date.day == 10

        assert product.item_info is not None
        assert len(product.genres) == 7
        assert len(product.series) == 1
        assert len(product.makers) == 1
        assert len(product.actresses) == 1
        assert len(product.directors) == 1
        assert len(product.labels) == 1

        genre_names = [g.name for g in product.genres]
        assert "ギャル" in genre_names
        assert "ぶっかけ" in genre_names
        assert "乱交" in genre_names

        assert product.series[0].name == "エンドレスセックス"
        assert product.makers[0].name == "プレステージ"
        assert product.actresses[0].name == "AIKA"
        assert product.directors[0].name == "マンハッタン木村"
        assert product.labels[0].name == "ABSOLUTELY PERFECT"

        assert product.jancode == "4571471003921"
        assert product.maker_product == "ABP-477"
        assert product.stock == "empty"

        assert len(product.directory) == 1
        assert product.directory[0].name == "DVD"

        assert product.raw_data is not None
        assert product.raw_data["content_id"] == cid

    async def test_product_with_nonexistent_cid(self, async_dmm_client):
        """Test retrieving a product with non-existent CID."""

        cid = "nonexistent99999"
        product = await async_dmm_client.get_product_by_cid(cid, site="FANZA")

        assert product is None

    async def test_product_by_product_id(self, async_dmm_client):
        """Test retrieving a single product by product ID."""

        product_id = "ABP-477"
        product = await async_dmm_client.get_product_by_product_id(
            product_id, site="FANZA"
        )

        assert product is not None
        assert isinstance(product, Product)

        assert product.service_code == "mono"
        assert product.service_name == "通販"
        assert product.floor_code == "dvd"
        assert product.floor_name == "DVD"
        assert product.content_id == "118abp477"
        assert product.title == "エンドレスセックス AIKA"
        assert product.maker_product == "ABP-477"

        assert product.item_info is not None
        assert len(product.genres) == 7
        assert len(product.actresses) == 1
        assert product.actresses[0].name == "AIKA"

    async def test_product_by_product_id_nonexistent(self, async_dmm_client):
        """Test retrieving a product with non-existent product ID."""

        product_id = "NONEXIST-999"
        product = await async_dmm_client.get_product_by_product_id(
            product_id, site="FANZA"
        )

        assert product is None

    async def test_multiple_concurrent_requests(self, async_dmm_client):
        """Test multiple concurrent API requests."""

        results = await asyncio.gather(
            async_dmm_client.get_products(
                site="FANZA", service="digital", floor="videoa", hits=2
            ),
            async_dmm_client.get_products(
                site="FANZA", service="ebook", floor="comic", hits=2
            ),
            async_dmm_client.get_products(
                site="DMM.com", service="mono", floor="book", hits=2
            ),
        )

        assert len(results) == 3
        assert all(isinstance(products, list) for products in results)
        assert all(len(products) <= 2 for products in results)

    async def test_session_reuse_across_requests(self, async_dmm_client):
        """Test that session is reused across multiple requests."""

        products1 = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        products2 = await async_dmm_client.get_products(
            site="FANZA", service="digital", floor="videoa", hits=1
        )

        assert len(products1) >= 0
        assert len(products2) >= 0
        assert async_dmm_client._session is not None
        assert not async_dmm_client._session.closed
