"""
py-dmm: A Python client library for the DMM API.

This package provides a simple and intuitive interface for interacting with
the DMM (Digital Media Mart) API.
"""

__version__ = "0.0.2"
__author__ = "Richard Nguyen"
__email__ = "richard@richardhnguyen.com"
__license__ = "MIT"

from .client import DMMClient
from .exceptions import DMMAPIError, DMMAuthError, DMMError
from .product import (
    ApiRequest,
    ApiResponse,
    ApiResult,
    Directory,
    ImageURL,
    ItemDetails,
    ItemInfo,
    Prices,
    Product,
    RequestParameters,
    Review,
    SampleImages,
    SearchResult,
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
    "SampleImages",
    "Prices",
    "ItemInfo",
    "ItemDetails",
    "Directory",
]
