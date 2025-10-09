"""
py-dmm: A Python client library for the DMM API.

This package provides a simple and intuitive interface for interacting with
the DMM (Digital Media Mart) API.
"""

__version__ = "0.1.0"
__author__ = "Richard Nguyen"
__email__ = "richard@example.com"
__license__ = "MIT"

from .client import DMMClient

__all__ = [
    "DMMClient",
]
