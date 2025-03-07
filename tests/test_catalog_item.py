from unittest.mock import MagicMock


class TestCatalogItem:
    """Tests for the CatalogItem resource."""

    def test_get_item(self, bricklink_client, mock_oauth_session):
        """Test getting item details."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {
                "no": "75281-1",
                "name": "Anakin's Jedi Interceptor",
                "type": "SET",
                "category_id": 65,
                "year_released": 2020,
                "weight": "360.00",
                "dim_x": "28.20",
                "dim_y": "6.10",
                "dim_z": "26.20",
            },
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.catalog_item.get_item("SET", "75281-1")

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/items/SET/75281-1", params=None
        )

        # Verify response was processed correctly
        assert result["no"] == "75281-1"
        assert result["name"] == "Anakin's Jedi Interceptor"
        assert result["year_released"] == 2020
        assert result["weight"] == "360.00"

    def test_get_item_image(self, bricklink_client, mock_oauth_session):
        """Test getting item image URL."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {
                "type": "SET",
                "no": "75281-1",
                "color_id": 0,
                "thumbnail_url": "https://img.bricklink.com/ItemImage/TN/0/75281-1.png",
                "large_url": "https://img.bricklink.com/ItemImage/ON/0/75281-1.png",
            },
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.catalog_item.get_item_image("SET", "75281-1", 0)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/items/SET/75281-1/images/0",
            params=None,
        )

        # Verify response was processed correctly
        assert (
            result["thumbnail_url"]
            == "https://img.bricklink.com/ItemImage/TN/0/75281-1.png"
        )
        assert (
            result["large_url"]
            == "https://img.bricklink.com/ItemImage/ON/0/75281-1.png"
        )

    def test_get_supersets(self, bricklink_client, mock_oauth_session):
        """Test getting supersets."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "color_id": 0,
                    "entries": [
                        {
                            "item": {
                                "no": "10221-1",
                                "name": "Super Star Destroyer",
                                "type": "SET",
                                "category_id": 65,
                            },
                            "quantity": 4,
                        }
                    ],
                }
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.catalog_item.get_supersets("PART", "2654", 15)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/items/PART/2654/supersets",
            params={"color_id": 15},
        )

        # Verify response was processed correctly
        assert len(result) == 1
        assert result[0]["color_id"] == 0
        assert result[0]["entries"][0]["item"]["name"] == "Super Star Destroyer"
        assert result[0]["entries"][0]["quantity"] == 4

    def test_get_subsets(self, bricklink_client, mock_oauth_session):
        """Test getting subsets."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "match_no": "75281-1",
                    "entries": [
                        {
                            "item": {
                                "no": "3039",
                                "name": "Slope 45 2 x 2",
                                "type": "PART",
                                "category_id": 38,
                            },
                            "color_id": 85,
                            "quantity": 2,
                            "extra_quantity": 0,
                            "is_alternate": False,
                            "is_counterpart": False,
                        }
                    ],
                }
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.catalog_item.get_subsets(
            "SET", "75281-1", box=True, instruction=True
        )

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/items/SET/75281-1/subsets",
            params={
                "color_id": None,
                "box": True,
                "instruction": True,
                "break_minifigs": False,
                "break_subsets": False,
            },
        )

        # Verify response was processed correctly
        assert result[0]["match_no"] == "75281-1"
        assert result[0]["entries"][0]["item"]["name"] == "Slope 45 2 x 2"
        assert result[0]["entries"][0]["quantity"] == 2

    def test_get_price_guide(self, bricklink_client, mock_oauth_session):
        """Test getting price guide."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {
                "item": {
                    "no": "75281-1",
                    "type": "SET",
                    "name": "Anakin's Jedi Interceptor",
                },
                "new_or_used": "N",
                "currency_code": "EUR",
                "min_price": "35.90",
                "max_price": "45.99",
                "avg_price": "41.27",
                "qty_avg_price": "43.00",
                "unit_quantity": 25,
                "total_quantity": 25,
                "price_detail": [
                    {"quantity": 1, "unit_price": "41.95"},
                    {"quantity": 2, "unit_price": "35.90"},
                ],
            },
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.catalog_item.get_price_guide(
            "SET", "75281-1", guide_type="sold", new_or_used="N", region="europe"
        )

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/items/SET/75281-1/price",
            params={
                "color_id": None,
                "guide_type": "sold",
                "new_or_used": "N",
                "country_code": None,
                "region": "europe",
                "currency_code": None,
                "vat": "N",
            },
        )

        # Verify response was processed correctly
        assert result["item"]["name"] == "Anakin's Jedi Interceptor"
        assert result["currency_code"] == "EUR"
        assert result["avg_price"] == "41.27"

    def test_get_known_colors(self, bricklink_client, mock_oauth_session):
        """Test getting known colors."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "color_id": 1,
                    "color_name": "Blue",
                    "color_code": "0055BF",
                    "quantity": 125,
                },
                {
                    "color_id": 5,
                    "color_name": "Red",
                    "color_code": "C91A09",
                    "quantity": 98,
                },
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.catalog_item.get_known_colors("PART", "3039")

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/items/PART/3039/colors", params=None
        )

        # Verify response was processed correctly
        assert len(result) == 2
        assert result[0]["color_name"] == "Blue"
        assert result[1]["color_name"] == "Red"
