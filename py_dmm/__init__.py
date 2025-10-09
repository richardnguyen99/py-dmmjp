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
from .exceptions import DMMError, DMMAPIError, DMMAuthError
from .product import (
    Product,
    ApiResponse,
    ApiResult,
    ApiRequest,
    RequestParameters,
    SearchResult,
    Review,
    ImageURL,
    SampleImages,
    Prices,
    ItemInfo,
    ItemDetails,
    Directory,
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
