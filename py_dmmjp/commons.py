"""
Common data models shared across different DMM API endpoints.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RequestParameters:
    """
    Represents the request parameters from the API response.
    """

    api_id: str
    "DMM API identifier for the request (e.g., 'your_api_id')"

    affiliate_id: str
    "Affiliate program identifier (e.g., 'affiliate_code-001')"

    site: str
    "Site code for DMM services (e.g., 'DMM.co.jp', 'DMM.com')"

    service: str
    "Service type (e.g., 'digital', 'mono', 'pcgame')"

    floor: str
    "Floor/section code (e.g., 'videoa', 'dvd', 'book')"

    keyword: Optional[str] = None
    "Search keyword if applicable (e.g., 'アダルト', '新作')"

    output: str = "json"
    "Response format, typically 'json' or 'xml'"

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
    "Request parameters used for the API call"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiRequest":
        """Create ApiRequest from dictionary."""

        return cls(parameters=RequestParameters.from_dict(data.get("parameters", {})))
