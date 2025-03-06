from unittest.mock import patch

from bricklink_py.bricklink import Bricklink


class TestBricklink:
    """Tests for the main Bricklink client."""

    def test_init(self):
        """Test that the client initializes with correct credentials."""
        with patch("bricklink_py.bricklink.OAuth1Session") as mock_oauth:
            _ = Bricklink(
                consumer_key="test_key",
                consumer_secret="test_secret",
                token="test_token",
                token_secret="test_token_secret",
            )

            # Verify OAuth1Session was created with the right credentials
            mock_oauth.assert_called_once_with(
                client_key="test_key",
                client_secret="test_secret",
                resource_owner_key="test_token",
                resource_owner_secret="test_token_secret",
            )

    def test_resource_initialization(self, bricklink_client):
        """Test that all API resources are properly initialized."""
        # Check that all resources are properly initialized
        assert bricklink_client.order is not None
        assert bricklink_client.store_inventory is not None
        assert bricklink_client.catalog_item is not None
        assert bricklink_client.feedback is not None
        assert bricklink_client.color is not None
        assert bricklink_client.category is not None
        assert bricklink_client.push_notification is not None
        assert bricklink_client.coupon is not None
        assert bricklink_client.setting is not None
        assert bricklink_client.member is not None
        assert bricklink_client.item_mapping is not None

        # Verify that OAuth session is passed to each resource
        assert bricklink_client.order._oauth_session == bricklink_client.oauth_session
        assert (
            bricklink_client.store_inventory._oauth_session
            == bricklink_client.oauth_session
        )
        assert (
            bricklink_client.catalog_item._oauth_session
            == bricklink_client.oauth_session
        )
