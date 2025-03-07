from unittest.mock import MagicMock, patch

import pytest

from bricklink_py.utils import (
    AuthenticationError,
    BaseResource,
    BricklinkError,
    RateLimitError,
    ResourceNotFoundError,
    handle_response,
    request,
)


class TestBaseResource:
    """Tests for the BaseResource class."""

    def test_init(self, mock_oauth_session):
        """Test initialization with OAuth session."""
        resource = BaseResource(mock_oauth_session)
        assert resource._oauth_session == mock_oauth_session

    def test_request_method(self, base_resource, mock_oauth_session):
        """Test the _request method."""
        with patch("bricklink_py.utils.request") as mock_request:
            mock_request.return_value = {"test": "data"}

            # Test a GET request
            result = base_resource._request("get", "test_uri", {"param": "value"})

            # Verify request was called with correct arguments
            mock_request.assert_called_once_with(
                "get", mock_oauth_session, "test_uri", {"param": "value"}, None
            )
            assert result == {"test": "data"}

    def test_request_method_with_error(self, base_resource):
        """Test the _request method when an error occurs."""
        with patch("bricklink_py.utils.request") as mock_request:
            # Simulate a BricklinkError
            mock_request.side_effect = BricklinkError(404, "Not found")

            # Verify the error is propagated
            with pytest.raises(BricklinkError):
                base_resource._request("get", "test_uri")


class TestHandleResponse:
    """Tests for the handle_response function."""

    def test_success_response(self, mock_response):
        """Test handling a successful response."""
        response = mock_response(
            200, {"meta": {"code": 200}, "data": {"test": "success"}}
        )
        result = handle_response(response)
        assert result == {"test": "success"}

    def test_not_found_error(self, mock_response):
        """Test handling a 404 error."""
        response = mock_response(404, {"meta": {"code": 404, "message": "Not found"}})
        with pytest.raises(ResourceNotFoundError) as excinfo:
            handle_response(response)
        assert excinfo.value.status_code == 404
        assert "Not found" in excinfo.value.message

    def test_rate_limit_error(self, mock_response):
        """Test handling a rate limit error."""
        response = mock_response(
            429, {"meta": {"code": 429, "message": "Rate limit exceeded"}}
        )
        with pytest.raises(RateLimitError) as excinfo:
            handle_response(response)
        assert excinfo.value.status_code == 429

    def test_authentication_error(self, mock_response):
        """Test handling an authentication error."""
        response = mock_response(
            401, {"meta": {"code": 401, "message": "Unauthorized"}}
        )
        with pytest.raises(AuthenticationError) as excinfo:
            handle_response(response)
        assert excinfo.value.status_code == 401


class TestRequest:
    """Tests for the request function."""

    def test_get_request(self, mock_oauth_session):
        """Test making a GET request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"key": "value"},
        }
        mock_oauth_session.get.return_value = mock_response

        result = request("get", mock_oauth_session, "test_endpoint", {"param": "value"})

        # Verify OAuth session's get method was called correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/test_endpoint",
            params={"param": "value"},
        )
        assert result == {"key": "value"}

    def test_post_request(self, mock_oauth_session):
        """Test making a POST request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"created": True},
        }
        mock_oauth_session.post.return_value = mock_response

        body = {"name": "test"}
        result = request("post", mock_oauth_session, "test_endpoint", None, body)

        # Verify OAuth session's post method was called correctly
        mock_oauth_session.post.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/test_endpoint",
            params=None,
            json=body,
        )
        assert result == {"created": True}

    def test_put_request(self, mock_oauth_session):
        """Test making a PUT request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"updated": True},
        }
        mock_oauth_session.put.return_value = mock_response

        body = {"status": "updated"}
        result = request("put", mock_oauth_session, "test_endpoint", None, body)

        # Verify OAuth session's put method was called correctly
        mock_oauth_session.put.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/test_endpoint",
            params=None,
            json=body,
        )
        assert result == {"updated": True}

    def test_delete_request(self, mock_oauth_session):
        """Test making a DELETE request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"deleted": True},
        }
        mock_oauth_session.delete.return_value = mock_response

        result = request("delete", mock_oauth_session, "test_endpoint")

        # Verify OAuth session's delete method was called correctly
        mock_oauth_session.delete.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/test_endpoint", params=None
        )
        assert result == {"deleted": True}

    def test_invalid_method(self, mock_oauth_session):
        """Test with an invalid HTTP method."""
        with pytest.raises(ValueError) as excinfo:
            request("invalid", mock_oauth_session, "test_endpoint")
        assert "Unsupported HTTP method" in str(excinfo.value)
