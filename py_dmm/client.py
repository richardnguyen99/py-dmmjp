"""
Main client class for the py-dmm library.
"""

import requests

from typing import Optional, Dict, Any
from urllib.parse import urljoin


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
            raise KeyError("API_KEY and AFFILIATE_KEY are required")

        self._api_key = api_key
        self._affiliate_id = affiliate_id
        self._base_url = "https://api.dmm.com/affiliate/v3/".rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

    def __post_init__(self) -> None:
        """Post initialization process to set DMM Client"""

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
        url = urljoin(self._base_url, endpoint)

        if params is None:
            params = {}

        params["api_id"] = self._api_key
        params["affiliate_id"] = self._affiliate_id
        params["output"] = "json"

        response = self._session.get(url, params=params, timeout=self._timeout)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError as e:
            raise ValueError(f"Error while formatting DMM Response: {e}") from e

    def get_products(self) -> None:
        """API that allows you to get information about FANZA products."""
        pass

    def get_floors(self) -> None:
        """API that can get the floor list,"""
        pass

    def get_actresses(self) -> None:
        """API that can get actress information."""
        pass

    def get_genres(self) -> None:
        """API that can get the genre list."""
        pass

    def get_makers(self) -> None:
        """API that retrieves a list of makers."""
        pass

    def get_series(self) -> None:
        """API that retrieves a list of series."""
        pass

    def get_authors(self) -> None:
        """API that retrieves a list of authors."""
        pass

    def close(self) -> None:
        """Explicitly close the HTTP session."""
        self._session.close()

    def __del__(self) -> None:
        """Destructor to ensure the session is closed."""
        self.close()

    def __enter__(self) -> "DMMClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
