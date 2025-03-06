from unittest.mock import MagicMock


class TestColor:
    """Tests for the Color resource."""

    def test_get_color_list(self, bricklink_client, mock_oauth_session):
        """Test retrieving the list of colors."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "color_id": 1,
                    "color_name": "Blue",
                    "color_code": "0055BF",
                    "color_type": "Solid",
                },
                {
                    "color_id": 2,
                    "color_name": "Green",
                    "color_code": "257A3E",
                    "color_type": "Solid",
                },
                {
                    "color_id": 3,
                    "color_name": "Dark Turquoise",
                    "color_code": "008F9B",
                    "color_type": "Solid",
                },
                {
                    "color_id": 4,
                    "color_name": "Red",
                    "color_code": "C91A09",
                    "color_type": "Solid",
                },
                {
                    "color_id": 5,
                    "color_name": "Dark Pink",
                    "color_code": "C870A0",
                    "color_type": "Solid",
                },
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.color.get_color_list()

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/colors", params=None
        )

        # Verify response was processed correctly
        assert len(result) == 5
        assert result[0]["color_id"] == 1
        assert result[0]["color_name"] == "Blue"
        assert result[1]["color_id"] == 2
        assert result[1]["color_name"] == "Green"
        assert result[2]["color_id"] == 3
        assert result[2]["color_name"] == "Dark Turquoise"

    def test_get_color(self, bricklink_client, mock_oauth_session):
        """Test retrieving a specific color."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {
                "color_id": 4,
                "color_name": "Red",
                "color_code": "C91A09",
                "color_type": "Solid",
            },
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.color.get_color(4)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/colors/4", params=None
        )

        # Verify response was processed correctly
        assert result["color_id"] == 4
        assert result["color_name"] == "Red"
        assert result["color_code"] == "C91A09"
        assert result["color_type"] == "Solid"
