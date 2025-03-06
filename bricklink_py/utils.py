from typing import Any

from requests_oauthlib import OAuth1Session

API_BASE_URL = "https://api.bricklink.com/api/store/v1/"


class BricklinkError(Exception):
    """Base exception for Bricklink API errors"""

    def __init__(self, status_code: int, message: str, response_data: dict = None):
        self.status_code = status_code
        self.message = message
        self.response_data = response_data or {}
        super().__init__(f"Bricklink API Error ({status_code}): {message}")


class ResourceNotFoundError(BricklinkError):
    """Raised when a resource is not found (404)"""

    pass


class RateLimitError(BricklinkError):
    """Raised when API rate limit is exceeded"""

    pass


class AuthenticationError(BricklinkError):
    """Raised for authentication issues"""

    pass


class BaseResource:
    """Base class for all Bricklink API resources with common utilities"""

    def __init__(self, oauth_session: OAuth1Session):
        """Initialize with OAuth session"""
        self._oauth_session = oauth_session

    def _request(
        self, method: str, uri: str, params: dict = None, body: dict = None
    ) -> Any:
        """Wrapper for the request function with error handling"""
        try:
            return request(method, self._oauth_session, uri, params, body)
        except BricklinkError:
            raise
        except Exception:
            raise


def handle_response(response):
    """Process API response and handle errors appropriately"""
    try:
        response_data = response.json()
    except ValueError:
        response.raise_for_status()
        return response

    if "meta" in response_data and response_data["meta"]["code"] != 200:
        error_code = response_data["meta"]["code"]
        error_message = response_data["meta"].get("message", "Unknown error")

        if error_code == 404:
            raise ResourceNotFoundError(error_code, error_message, response_data)
        elif error_code == 429:
            raise RateLimitError(error_code, "Rate limit exceeded", response_data)
        elif error_code in (401, 403):
            raise AuthenticationError(error_code, error_message, response_data)
        else:
            raise BricklinkError(error_code, error_message, response_data)

    if "data" in response_data:
        return response_data["data"]

    return response_data


def request(
    method: str,
    oauth_session: OAuth1Session,
    uri: str,
    params: dict = None,
    body: dict = None,
) -> Any:
    """Send a request to the specified URI using the provided
    method and OAuth session.

    Arguments:
        method -- The HTTP method to use for the request.
        oauth_session -- The OAuth object used for authentication.
        uri -- The URI to send the request to.

    Keyword Arguments:
        params -- The parameters to include in the request. (default: {{}})
        body -- The body to include in the request data. (default: {{}})

    Raises:
        BricklinkError: For API-specific errors.
        requests.RequestException: For general request errors.

    Returns:
        requests.Response: The response object returned from the request.
    """
    url = f"{API_BASE_URL}{uri}"

    try:
        if method.lower() == "get":
            response = oauth_session.get(url, params=params)
        elif method.lower() == "post":
            response = oauth_session.post(url, params=params, json=body)
        elif method.lower() == "put":
            response = oauth_session.put(url, params=params, json=body)
        elif method.lower() == "delete":
            response = oauth_session.delete(url, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return handle_response(response)

    except BricklinkError:
        raise
    except Exception:
        raise
