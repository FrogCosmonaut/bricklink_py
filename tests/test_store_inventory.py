from unittest.mock import MagicMock


class TestStoreInventory:
    """Tests for the StoreInventory resource."""

    def test_get_store_inventories(self, bricklink_client, mock_oauth_session):
        """Test retrieving store inventories with filtering."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "inventory_id": 123456,
                    "item": {
                        "no": "3039",
                        "name": "Slope 45 2 x 2",
                        "type": "PART",
                        "category_id": 38,
                    },
                    "color_id": 1,
                    "color_name": "Blue",
                    "quantity": 20,
                    "new_or_used": "N",
                    "unit_price": "0.25",
                    "bind_id": 0,
                    "description": "New condition",
                    "remarks": "",
                    "bulk": 1,
                    "is_retain": False,
                    "is_stock_room": False,
                    "stock_room_id": None,
                    "date_created": "2022-12-01T08:00:00.000Z",
                    "my_cost": "0.15",
                    "sale_rate": 5,
                    "tier_quantity1": 10,
                    "tier_price1": "0.22",
                    "tier_quantity2": 50,
                    "tier_price2": "0.20",
                    "tier_quantity3": 100,
                    "tier_price3": "0.18",
                },
                {
                    "inventory_id": 123457,
                    "item": {
                        "no": "3040",
                        "name": "Slope 45 2 x 1",
                        "type": "PART",
                        "category_id": 38,
                    },
                    "color_id": 5,
                    "color_name": "Red",
                    "quantity": 15,
                    "new_or_used": "N",
                    "unit_price": "0.20",
                    "bind_id": 0,
                    "description": "New condition",
                    "remarks": "",
                    "bulk": 1,
                    "is_retain": False,
                    "is_stock_room": True,
                    "stock_room_id": "A",
                    "date_created": "2022-12-05T10:30:00.000Z",
                    "my_cost": "0.12",
                    "sale_rate": 5,
                    "tier_quantity1": 10,
                    "tier_price1": "0.18",
                    "tier_quantity2": 50,
                    "tier_price2": "0.16",
                    "tier_quantity3": 100,
                    "tier_price3": "0.15",
                },
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method with filters
        result = bricklink_client.store_inventory.get_store_inventories(
            item_type="PART", status="Y,S", category_id=38, color_id="1,5"
        )

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/inventories",
            params={
                "item_type": "PART",
                "status": "Y,S",
                "category_id": 38,
                "color_id": "1,5",
            },
        )

        # Verify response was processed correctly
        assert len(result) == 2
        assert result[0]["inventory_id"] == 123456
        assert result[0]["item"]["name"] == "Slope 45 2 x 2"
        assert result[0]["color_name"] == "Blue"
        assert result[1]["inventory_id"] == 123457
        assert result[1]["item"]["name"] == "Slope 45 2 x 1"
        assert result[1]["color_name"] == "Red"

    def test_get_store_inventory(self, bricklink_client, mock_oauth_session):
        """Test retrieving a specific inventory item."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {
                "inventory_id": 123456,
                "item": {
                    "no": "3039",
                    "name": "Slope 45 2 x 2",
                    "type": "PART",
                    "category_id": 38,
                },
                "color_id": 1,
                "color_name": "Blue",
                "quantity": 20,
                "new_or_used": "N",
                "unit_price": "0.25",
                "bind_id": 0,
                "description": "New condition",
                "remarks": "",
                "bulk": 1,
                "is_retain": False,
                "is_stock_room": False,
                "stock_room_id": None,
                "date_created": "2022-12-01T08:00:00.000Z",
                "my_cost": "0.15",
                "sale_rate": 5,
                "tier_quantity1": 10,
                "tier_price1": "0.22",
                "tier_quantity2": 50,
                "tier_price2": "0.20",
                "tier_quantity3": 100,
                "tier_price3": "0.18",
            },
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.store_inventory.get_store_inventory(123456)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/inventories/123456", params=None
        )

        # Verify response was processed correctly
        assert result["inventory_id"] == 123456
        assert result["item"]["name"] == "Slope 45 2 x 2"
        assert result["color_name"] == "Blue"
        assert result["quantity"] == 20

    def test_create_store_inventory(self, bricklink_client, mock_oauth_session):
        """Test creating a new inventory item."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"inventory_id": 123458},
        }
        mock_oauth_session.post.return_value = mock_response

        # Call method
        inventory_data = {
            "item": {"no": "3039", "type": "PART"},
            "color_id": 1,
            "quantity": 15,
            "unit_price": "0.25",
            "new_or_used": "N",
            "description": "New parts",
            "remarks": "From bulk lot",
            "bulk": 1,
            "is_retain": False,
            "is_stock_room": False,
            "my_cost": "0.15",
            "sale_rate": 5,
            "tier_quantity1": 10,
            "tier_price1": "0.22",
            "tier_quantity2": 50,
            "tier_price2": "0.20",
            "tier_quantity3": 100,
            "tier_price3": "0.18",
        }
        result = bricklink_client.store_inventory.create_store_inventory(inventory_data)

        # Verify request was made correctly
        mock_oauth_session.post.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/inventories",
            params=None,
            json=inventory_data,
        )

        # Verify response was processed correctly
        assert result["inventory_id"] == 123458

    def test_create_store_inventories(self, bricklink_client, mock_oauth_session):
        """Test creating multiple inventory items."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [{"inventory_id": 123458}, {"inventory_id": 123459}],
        }
        mock_oauth_session.post.return_value = mock_response

        # Call method
        inventory_data = [
            {
                "item": {"no": "3039", "type": "PART"},
                "color_id": 1,
                "quantity": 15,
                "unit_price": "0.25",
                "new_or_used": "N",
            },
            {
                "item": {"no": "3040", "type": "PART"},
                "color_id": 5,
                "quantity": 10,
                "unit_price": "0.20",
                "new_or_used": "N",
            },
        ]
        result = bricklink_client.store_inventory.create_store_inventories(
            inventory_data
        )

        # Verify request was made correctly
        mock_oauth_session.post.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/inventories",
            params=None,
            json=inventory_data,
        )

        # Verify response was processed correctly
        assert len(result) == 2
        assert result[0]["inventory_id"] == 123458
        assert result[1]["inventory_id"] == 123459

    def test_update_store_inventory(self, bricklink_client, mock_oauth_session):
        """Test updating an inventory item."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"inventory_id": 123456, "unit_price": "0.30"},
        }
        mock_oauth_session.put.return_value = mock_response

        # Call method
        update_data = {"unit_price": "0.30", "quantity": 25, "remarks": "Updated stock"}
        result = bricklink_client.store_inventory.update_store_inventory(
            123456, update_data
        )

        # Verify request was made correctly
        mock_oauth_session.put.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/inventories/123456",
            params=None,
            json=update_data,
        )

        # Verify response was processed correctly
        assert result["inventory_id"] == 123456
        assert result["unit_price"] == "0.30"

    def test_delete_store_inventory(self, bricklink_client, mock_oauth_session):
        """Test deleting an inventory item."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"inventory_id": 123456, "result": "deleted"},
        }
        mock_oauth_session.delete.return_value = mock_response

        # Call method
        result = bricklink_client.store_inventory.delete_store_inventory(123456)

        # Verify request was made correctly
        mock_oauth_session.delete.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/inventories/123456", params=None
        )

        # Verify response was processed correctly
        assert result["inventory_id"] == 123456
        assert result["result"] == "deleted"
