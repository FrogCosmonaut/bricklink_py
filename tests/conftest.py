import pytest
from unittest.mock import MagicMock, patch
from requests_oauthlib import OAuth1Session

from bricklink_py.bricklink import Bricklink
from bricklink_py.utils import BaseResource


@pytest.fixture
def mock_oauth_session():
    """Create a mock OAuth1Session for testing."""
    mock_session = MagicMock(spec=OAuth1Session)
    
    # Configure the mock to return successful responses by default
    mock_response = MagicMock()
    mock_response.json.return_value = {'meta': {'code': 200}, 'data': {}}
    
    # Configure standard HTTP methods
    mock_session.get.return_value = mock_response
    mock_session.post.return_value = mock_response
    mock_session.put.return_value = mock_response
    mock_session.delete.return_value = mock_response
    
    return mock_session


@pytest.fixture
def bricklink_client(mock_oauth_session):
    """Create a Bricklink client with mocked OAuth session."""
    with patch('bricklink_py.bricklink.OAuth1Session', return_value=mock_oauth_session):
        client = Bricklink(
            consumer_key='test_consumer_key',
            consumer_secret='test_consumer_secret',
            token='test_token',
            token_secret='test_token_secret'
        )
        return client


@pytest.fixture
def base_resource(mock_oauth_session):
    """Create a BaseResource with mocked OAuth session for testing."""
    return BaseResource(mock_oauth_session)


@pytest.fixture
def mock_response():
    """Create a standard mock response with helper methods."""
    class MockResponse:
        def __init__(self, status_code=200, json_data=None, text=""):
            self.status_code = status_code
            self._json_data = json_data or {'meta': {'code': status_code}, 'data': {}}
            self.text = text
            
        def json(self):
            return self._json_data
            
        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP Error: {self.status_code}")
    
    return MockResponse


@pytest.fixture
def mock_error_response():
    """Create an error mock response."""
    def _create_error(code=404, message="Not found"):
        mock = MagicMock()
        mock.json.return_value = {
            'meta': {
                'code': code,
                'message': message
            }
        }
        return mock
    
    return _create_error
