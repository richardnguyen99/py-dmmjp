"""
Data models for the py-dmm library.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Review:
    """Represents product review data."""

    count: int
    average: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Review":
        """Create Review from dictionary."""
        return cls(
            count=int(data.get("count", 0)), average=str(data.get("average", "0"))
        )


@dataclass
class ImageURL:
    """Represents product image URLs."""

    list: Optional[str] = None
    small: Optional[str] = None
    large: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImageURL":
        """Create ImageURL from dictionary."""
        return cls(
            list=data.get("list"), small=data.get("small"), large=data.get("large")
        )


@dataclass
class SampleImages:
    """Represents sample image data."""

    sample_s: Optional[Dict[str, List[str]]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SampleImages":
        """Create SampleImages from dictionary."""
        return cls(sample_s=data.get("sample_s"))


@dataclass
class Prices:
    """Represents product pricing data."""

    price: Optional[str] = None
    list_price: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prices":
        """Create Prices from dictionary."""
        return cls(price=data.get("price"), list_price=data.get("list_price"))

    @property
    def price_int(self) -> Optional[int]:
        """Get price as integer."""
        return int(self.price) if self.price else None

    @property
    def list_price_int(self) -> Optional[int]:
        """Get list price as integer."""
        return int(self.list_price) if self.list_price else None


@dataclass
class ItemInfo:
    """Represents detailed item information."""

    id: int
    name: str
    ruby: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ItemInfo":
        """Create ItemInfo from dictionary."""
        return cls(id=data["id"], name=data["name"], ruby=data.get("ruby"))


@dataclass
class ItemDetails:
    """Represents all item details including genres, series, etc."""

    genre: List[ItemInfo] = field(default_factory=list)
    series: List[ItemInfo] = field(default_factory=list)
    maker: List[ItemInfo] = field(default_factory=list)
    actress: List[ItemInfo] = field(default_factory=list)
    director: List[ItemInfo] = field(default_factory=list)
    label: List[ItemInfo] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ItemDetails":
        """Create ItemDetails from dictionary."""
        return cls(
            genre=[ItemInfo.from_dict(item) for item in data.get("genre", [])],
            series=[ItemInfo.from_dict(item) for item in data.get("series", [])],
            maker=[ItemInfo.from_dict(item) for item in data.get("maker", [])],
            actress=[ItemInfo.from_dict(item) for item in data.get("actress", [])],
            director=[ItemInfo.from_dict(item) for item in data.get("director", [])],
            label=[ItemInfo.from_dict(item) for item in data.get("label", [])],
        )


@dataclass
class Directory:
    """Represents directory information."""

    id: int
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Directory":
        """Create Directory from dictionary."""
        return cls(id=data["id"], name=data["name"])


@dataclass
class Product:
    """Represents a product from the DMM API."""

    service_code: str
    service_name: str
    floor_code: str
    floor_name: str
    category_name: str
    content_id: str
    product_id: str
    title: str
    volume: int
    date: Optional[datetime] = None

    url: Optional[str] = None
    affiliate_url: Optional[str] = None

    image_url: Optional[ImageURL] = None
    sample_image_url: Optional[SampleImages] = None

    prices: Optional[Prices] = None
    review: Optional[Review] = None

    jancode: Optional[str] = None
    maker_product: Optional[str] = None
    stock: Optional[str] = None

    iteminfo: Optional[ItemDetails] = None
    directory: List[Directory] = field(default_factory=list)

    _raw_data: Optional[Dict[str, Any]] = field(default=None, repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """
        Create a Product instance from a dictionary.

        Args:
            data: Dictionary containing product data from DMM API.

        Returns:
            Product instance.
        """
        date = None
        if "date" in data and data["date"]:
            try:
                date = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                date = None

        image_url = (
            ImageURL.from_dict(data.get("imageURL", {}))
            if data.get("imageURL")
            else None
        )

        sample_image_url = (
            SampleImages.from_dict(data.get("sampleImageURL", {}))
            if data.get("sampleImageURL")
            else None
        )

        prices = (
            Prices.from_dict(data.get("prices", {})) if data.get("prices") else None
        )

        review = (
            Review.from_dict(data.get("review", {})) if data.get("review") else None
        )

        iteminfo = (
            ItemDetails.from_dict(data.get("iteminfo", {}))
            if data.get("iteminfo")
            else None
        )

        directory = [
            Directory.from_dict(dir_data) for dir_data in data.get("directory", [])
        ]

        return cls(
            service_code=data.get("service_code", ""),
            service_name=data.get("service_name", ""),
            floor_code=data.get("floor_code", ""),
            floor_name=data.get("floor_name", ""),
            category_name=data.get("category_name", ""),
            content_id=data.get("content_id", ""),
            product_id=data.get("product_id", ""),
            title=data.get("title", ""),
            volume=data.get("volume", 0),
            url=data.get("URL", ""),
            affiliate_url=data.get("affiliateURL", ""),
            image_url=image_url,
            sample_image_url=sample_image_url,
            prices=prices,
            review=review,
            date=date,
            jancode=data.get("jancode"),
            maker_product=data.get("maker_product"),
            stock=data.get("stock"),
            iteminfo=iteminfo,
            directory=directory,
            _raw_data=data.copy(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Product instance to a dictionary.

        Returns:
            Dictionary representation of the product.
        """
        result = {
            "service_code": self.service_code,
            "service_name": self.service_name,
            "floor_code": self.floor_code,
            "floor_name": self.floor_name,
            "category_name": self.category_name,
            "content_id": self.content_id,
            "product_id": self.product_id,
            "title": self.title,
            "volume": self.volume,
            "URL": self.url,
            "affiliateURL": self.affiliate_url,
            "jancode": self.jancode,
            "maker_product": self.maker_product,
            "stock": self.stock,
        }

        if self.date:
            result["date"] = self.date.strftime("%Y-%m-%d %H:%M:%S")

        return result

    @property
    def raw_data(self) -> Optional[Dict[str, Any]]:
        """Access to raw API response data."""
        return self._raw_data

    @property
    def genres(self) -> List[ItemInfo]:
        """Get product genres."""
        return self.iteminfo.genre if self.iteminfo else []

    @property
    def actresses(self) -> List[ItemInfo]:
        """Get product actresses."""
        return self.iteminfo.actress if self.iteminfo else []

    @property
    def makers(self) -> List[ItemInfo]:
        """Get product makers."""
        return self.iteminfo.maker if self.iteminfo else []

    @property
    def series(self) -> List[ItemInfo]:
        """Get product series."""
        return self.iteminfo.series if self.iteminfo else []

    @property
    def directors(self) -> List[ItemInfo]:
        """Get product directors."""
        return self.iteminfo.director if self.iteminfo else []

    @property
    def labels(self) -> List[ItemInfo]:
        """Get product labels."""
        return self.iteminfo.label if self.iteminfo else []

    @property
    def sample_images(self) -> List[str]:
        """Get sample image URLs."""
        if (
            self.sample_image_url
            and self.sample_image_url.sample_s
            and "image" in self.sample_image_url.sample_s
        ):
            return self.sample_image_url.sample_s["image"]
        return []

    @property
    def current_price(self) -> Optional[int]:
        """Get current price as integer."""
        return self.prices.price_int if self.prices else None

    @property
    def original_price(self) -> Optional[int]:
        """Get original list price as integer."""
        return self.prices.list_price_int if self.prices else None

    @property
    def review_count(self) -> int:
        """Get review count."""
        return self.review.count if self.review else 0

    @property
    def review_average(self) -> Optional[float]:
        """Get average review score as float."""
        if self.review and self.review.average:
            try:
                return float(self.review.average)
            except ValueError:
                return None
        return None


@dataclass
class RequestParameters:
    """Represents the request parameters from the API response."""

    api_id: str
    affiliate_id: str
    site: str
    service: str
    floor: str
    keyword: Optional[str] = None
    output: str = "json"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestParameters":
        """Create RequestParameters from dictionary."""
        return cls(
            api_id=data.get("api_id", ""),
            affiliate_id=data.get("affiliate_id", ""),
            site=data.get("site", ""),
            service=data.get("service", ""),
            floor=data.get("floor", ""),
            keyword=data.get("keyword"),
            output=data.get("output", "json"),
        )


@dataclass
class ApiRequest:
    """Represents the request section of the API response."""

    parameters: RequestParameters

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiRequest":
        """Create ApiRequest from dictionary."""
        return cls(parameters=RequestParameters.from_dict(data.get("parameters", {})))


@dataclass
class ApiResult:
    """Represents the result section of the API response."""

    status: int
    result_count: int
    total_count: int
    first_position: int
    items: List[Product] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiResult":
        """Create ApiResult from dictionary."""
        items = [Product.from_dict(item) for item in data.get("items", [])]

        return cls(
            status=data.get("status", 200),
            result_count=data.get("result_count", 0),
            total_count=data.get("total_count", 0),
            first_position=data.get("first_position", 1),
            items=items,
        )


@dataclass
class ApiResponse:
    """Represents the complete API response from DMM."""

    request: ApiRequest
    result: ApiResult
    _raw_response: Optional[Dict[str, Any]] = field(default=None, repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiResponse":
        """
        Create ApiResponse from the full API response dictionary.

        Args:
            data: Complete API response dictionary.

        Returns:
            ApiResponse instance.
        """
        return cls(
            request=ApiRequest.from_dict(data.get("request", {})),
            result=ApiResult.from_dict(data.get("result", {})),
            _raw_response=data.copy(),
        )

    @property
    def raw_response(self) -> Optional[Dict[str, Any]]:
        """Access to the complete raw API response."""
        return self._raw_response

    @property
    def products(self) -> List[Product]:
        """Get all products from the response."""
        return self.result.items

    @property
    def product_count(self) -> int:
        """Get the number of products returned."""
        return self.result.result_count

    @property
    def total_products(self) -> int:
        """Get the total number of products available."""
        return self.result.total_count

    @property
    def status(self) -> int:
        """Get the API response status."""
        return self.result.status


@dataclass
class SearchResult:
    """Represents search results from the DMM API (legacy compatibility)."""

    products: List[Product]
    total_count: int
    page: int = 1
    page_size: int = 20
    total_pages: int = 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """
        Create a SearchResult instance from a dictionary.

        Args:
            data: Dictionary containing search result data.

        Returns:
            SearchResult instance.
        """
        products = [
            Product.from_dict(product_data) for product_data in data.get("products", [])
        ]

        return cls(
            products=products,
            total_count=data.get("total_count", 0),
            page=data.get("page", 1),
            page_size=data.get("page_size", 20),
            total_pages=data.get("total_pages", 1),
        )

    @classmethod
    def from_api_response(
        cls, response: ApiResponse, page: int = 1, page_size: int = 20
    ) -> "SearchResult":
        """
        Create SearchResult from ApiResponse for backward compatibility.

        Args:
            response: ApiResponse instance.
            page: Current page number.
            page_size: Items per page.

        Returns:
            SearchResult instance.
        """
        total_pages = (response.total_products + page_size - 1) // page_size

        return cls(
            products=response.products,
            total_count=response.total_products,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
