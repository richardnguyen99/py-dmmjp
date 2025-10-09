"""
Main client class for the py-dmm library.
"""

import requests
import json
import requests.exceptions

from typing import Optional, Dict, Any, Literal, cast

from .exceptions import DMMError, DMMAPIError, DMMAuthError
from .product import ApiResponse


class DMMClient:
    """
    A client for interacting with the DMM API.

    Core class to handle main DMM API interactions.
    """

    def __init__(
        self,
        api_key: str,
        affiliate_id: str,
        timeout: int = 10,
    ) -> None:
        """
        Initialize the DMM client.

        Args:
            api_key: Your DMM API key for authentication.
            affiliate_id: Your DMM affiliate ID.
            timeout: Request timeout in seconds.

        Raises:
            DMMAuthError: If the API key is invalid or missing.
        """

        if (
            not api_key
            or not api_key.strip()
            or not affiliate_id
            or not affiliate_id.strip()
        ):
            raise DMMAuthError("API_KEY and AFFILIATE_KEY are required")

        self._api_key = api_key
        self._affiliate_id = affiliate_id
        self._base_url = "https://api.dmm.com/affiliate/v3"
        self._timeout = timeout
        self._session = requests.Session()

        self._session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the DMM API.

        Args:
            endpoint: API endpoint to call.
            params: Query parameters to include.
            method: HTTP method to use.

        Returns:
            JSON response data.

        Raises:
            DMMAPIError: If the API request fails.
            DMMAuthError: If authentication fails.
        """
        url = f"{self._base_url}{endpoint}"

        if params is None:
            params = {}

        params["api_id"] = self._api_key
        params["affiliate_id"] = self._affiliate_id
        params["output"] = "json"

        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            raise DMMAPIError("Request timed out") from e
        except requests.exceptions.ConnectionError as e:
            raise DMMAPIError("Connection error occurred") from e
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise DMMAuthError("Invalid API key or authentication failed") from e

            if response.status_code == 403:
                raise DMMAuthError(
                    "Access forbidden - check your API key permissions"
                ) from e

            raise DMMAPIError(
                f"HTTP {response.status_code}: {response.text}",
                status_code=response.status_code,
                response_data=response.text,
            ) from e
        except requests.exceptions.RequestException as e:
            raise DMMAPIError(f"Request failed: {str(e)}") from e

        try:
            return cast(Dict[str, Any], json.loads(response.text))
        except ValueError as e:
            raise DMMAPIError("Error while formatting DMM Response") from e

    def get_products(
        self,
        *,
        site: Literal["FANZA", "DMM.com"],
        service: Optional[str],
        floor: Optional[str],
        keyword: Optional[str] = None,
        hits: int = 20,
        offset: int = 1,
        sort: Optional[str] = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """
        API that allows you to get information about FANZA products.

        See more: https://affiliate.dmm.com/api/v3/itemlist.html

        Args:
            site (str): Site to search (`FANZA` or `DMM.com`)
            service (str, optional): Service code that the products can be retrieve from. Can be obtained from Floor API
            floor (str, optional): Floor code that the products can be retrieved from. Can be obtained from Floor API
            keyword (str, optional): Search keyword. Can be title, actress, product id, maker id, etc.
            hits (int, optional): Number of results to return (default: 20)
            offset (int, optional): Starting position (default: 1)
            sort (str, optional): Sort order (default: "rank")
            **kwargs: Additional parameters

        Returns:
            ApiResponse containing the product data and metadata

        Raises:
            DMMAPIError: If the API request fails
            DMMAuthError: If authentication fails
        """
        params = {
            "site": site,
            "service": service,
            "floor": floor,
            "hits": hits,
            "offset": offset,
        }

        if keyword:
            params["keyword"] = keyword

        if sort:
            params["sort"] = sort

        params.update(kwargs)

        try:
            response_data = self._make_request("/ItemList", params)
            return ApiResponse.from_dict(response_data)
        except Exception as e:
            if isinstance(e, (DMMError, DMMAPIError, DMMAuthError)):
                raise

            raise DMMAPIError(f"Failed to get products: {str(e)}") from e

    def get_floors(self) -> None:
        """API that can get the floor list,"""

    def get_actresses(self) -> None:
        """API that can get actress information."""

    def get_genres(self) -> None:
        """API that can get the genre list."""

    def get_makers(self) -> None:
        """API that retrieves a list of makers."""

    def get_series(self) -> None:
        """API that retrieves a list of series."""

    def get_authors(self) -> None:
        """API that retrieves a list of authors."""

    def close(self) -> None:
        """Explicitly close the HTTP session."""
        self._session.close()

    def __del__(self) -> None:
        """Destructor to ensure the session is closed."""
        if hasattr(self, "_session"):
            self.close()

    def __enter__(self) -> "DMMClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
