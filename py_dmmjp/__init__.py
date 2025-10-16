"""
py-dmmjp: A Python client library for the DMM API.

This package provides a simple and intuitive interface for interacting with
the DMM-JP API.
"""

__version__ = "0.0.6"
__author__ = "Richard Nguyen"
__email__ = "richard@richardhnguyen.com"
__license__ = "MIT"

from .actress import (
    Actress,
    ActressImageURL,
    ActressListURL,
    ActressSearchResponse,
    ActressSearchResult,
)
from .client import DMMClient
from .commons import ApiRequest, RequestParameters
from .exceptions import DMMAPIError, DMMAuthError, DMMError
from .floor import Floor, FloorListResponse, FloorListResult, Service, Site
from .product import (
    ApiResponse,
    ApiResult,
    Campaign,
    CDInfo,
    Delivery,
    Directory,
    ImageURL,
    ItemDetails,
    ItemInfo,
    Prices,
    Product,
    Review,
    SampleImage,
    SampleImages,
    SampleMovieURL,
    SearchResult,
    TachiyomiInfo,
)

__all__ = [
    "DMMClient",
    "DMMError",
    "DMMAPIError",
    "DMMAuthError",
    "Product",
    "ApiResponse",
    "ApiResult",
    "ApiRequest",
    "RequestParameters",
    "SearchResult",
    "Review",
    "ImageURL",
    "SampleImage",
    "SampleImages",
    "SampleMovieURL",
    "TachiyomiInfo",
    "Prices",
    "Delivery",
    "ItemInfo",
    "ItemDetails",
    "Directory",
    "CDInfo",
    "Campaign",
    "Actress",
    "ActressImageURL",
    "ActressListURL",
    "ActressSearchResponse",
    "ActressSearchResult",
    "Floor",
    "Site",
    "Service",
    "FloorListResponse",
    "FloorListResult",
]
