from unittest.mock import MagicMock


class TestOrder:
    """Tests for the Order resource."""

    def test_get_orders(self, bricklink_client, mock_oauth_session):
        """Test retrieving orders."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "order_id": 12345678,
                    "date_ordered": "2023-01-15T15:00:00.000Z",
                    "seller_name": "TestSeller",
                    "store_name": "Test Store",
                    "buyer_name": "TestBuyer",
                    "total_count": 5,
                    "unique_count": 3,
                    "status": "PENDING",
                    "payment": {"method": "PayPal", "status": "None"},
                    "cost": {
                        "subtotal": "25.00",
                        "grand_total": "30.00",
                        "currency_code": "USD",
                    },
                },
                {
                    "order_id": 12345679,
                    "date_ordered": "2023-01-20T10:00:00.000Z",
                    "seller_name": "TestSeller",
                    "store_name": "Test Store",
                    "buyer_name": "AnotherBuyer",
                    "total_count": 2,
                    "unique_count": 1,
                    "status": "PROCESSING",
                    "payment": {"method": "PayPal", "status": "Received"},
                    "cost": {
                        "subtotal": "15.00",
                        "grand_total": "20.00",
                        "currency_code": "USD",
                    },
                },
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.order.get_orders(
            direction="in", status="PENDING,PROCESSING"
        )

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders",
            params={"direction": "in", "status": "PENDING,PROCESSING", "filed": False},
        )

        # Verify response was processed correctly
        assert len(result) == 2
        assert result[0]["order_id"] == 12345678
        assert result[0]["status"] == "PENDING"
        assert result[1]["order_id"] == 12345679
        assert result[1]["status"] == "PROCESSING"

    def test_get_order(self, bricklink_client, mock_oauth_session):
        """Test retrieving a specific order."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {
                "order_id": 12345678,
                "date_ordered": "2023-01-15T15:00:00.000Z",
                "date_status_changed": "2023-01-15T15:05:00.000Z",
                "seller_name": "TestSeller",
                "store_name": "Test Store",
                "buyer_name": "TestBuyer",
                "total_count": 5,
                "unique_count": 3,
                "status": "PENDING",
                "payment": {"method": "PayPal", "status": "None", "date_paid": None},
                "shipping": {"method": "Standard", "address": {"country_code": "US"}},
                "cost": {
                    "subtotal": "25.00",
                    "grand_total": "30.00",
                    "currency_code": "USD",
                    "shipping": "5.00",
                },
                "disp_cost": {
                    "subtotal": "$25.00",
                    "grand_total": "$30.00",
                    "shipping": "$5.00",
                },
            },
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.order.get_order(12345678)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678", params=None
        )

        # Verify response was processed correctly
        assert result["order_id"] == 12345678
        assert result["buyer_name"] == "TestBuyer"
        assert result["status"] == "PENDING"
        assert result["cost"]["grand_total"] == "30.00"

    def test_get_order_items(self, bricklink_client, mock_oauth_session):
        """Test retrieving items for an order."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                [
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
                        "quantity": 2,
                        "unit_price": "0.25",
                        "disp_unit_price": "$0.25",
                        "unit_price_final": "0.25",
                        "disp_unit_price_final": "$0.25",
                        "extended_price": "0.50",
                        "disp_extended_price": "$0.50",
                        "extended_price_final": "0.50",
                        "disp_extended_price_final": "$0.50",
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
                        "quantity": 3,
                        "unit_price": "0.20",
                        "disp_unit_price": "$0.20",
                        "unit_price_final": "0.20",
                        "disp_unit_price_final": "$0.20",
                        "extended_price": "0.60",
                        "disp_extended_price": "$0.60",
                        "extended_price_final": "0.60",
                        "disp_extended_price_final": "$0.60",
                    },
                ]
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.order.get_order_items(12345678)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678/items", params=None
        )

        # Verify response was processed correctly
        assert len(result) == 1  # One batch
        assert len(result[0]) == 2  # Two items in the batch
        assert result[0][0]["item"]["name"] == "Slope 45 2 x 2"
        assert result[0][0]["quantity"] == 2
        assert result[0][1]["item"]["name"] == "Slope 45 2 x 1"
        assert result[0][1]["quantity"] == 3

    def test_get_order_messages(self, bricklink_client, mock_oauth_session):
        """Test retrieving messages for an order."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "message_id": 98765,
                    "subject": "Order Confirmation",
                    "body": "Thank you for your order!",
                    "from": "TestSeller",
                    "to": "TestBuyer",
                    "dateSent": "2023-01-15T15:30:00.000Z",
                },
                {
                    "message_id": 98766,
                    "subject": "Shipping Question",
                    "body": "When will this ship?",
                    "from": "TestBuyer",
                    "to": "TestSeller",
                    "dateSent": "2023-01-16T10:30:00.000Z",
                },
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.order.get_order_messages(12345678)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678/messages",
            params=None,
        )

        # Verify response was processed correctly
        assert len(result) == 2
        assert result[0]["subject"] == "Order Confirmation"
        assert result[1]["subject"] == "Shipping Question"

    def test_get_order_feedback(self, bricklink_client, mock_oauth_session):
        """Test retrieving feedback for an order."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": [
                {
                    "feedback_id": 54321,
                    "order_id": 12345678,
                    "from": "TestBuyer",
                    "to": "TestSeller",
                    "rating": "POSITIVE",
                    "comment": "Great seller, fast shipping!",
                    "date": "2023-01-20T12:00:00.000Z",
                }
            ],
        }
        mock_oauth_session.get.return_value = mock_response

        # Call method
        result = bricklink_client.order.get_order_feedback(12345678)

        # Verify request was made correctly
        mock_oauth_session.get.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678/feedback",
            params=None,
        )

        # Verify response was processed correctly
        assert len(result) == 1
        assert result[0]["rating"] == "POSITIVE"
        assert result[0]["comment"] == "Great seller, fast shipping!"

    def test_update_order(self, bricklink_client, mock_oauth_session):
        """Test updating an order."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"order_id": 12345678, "status": "UPDATED"},
        }
        mock_oauth_session.put.return_value = mock_response

        # Call method
        update_data = {
            "shipping": {
                "date_shipped": "2023-01-17T09:00:00.000Z",
                "tracking_no": "US12345678901",
                "tracking_link": "https://track.example.com/US12345678901",
                "method_id": 1,
            },
            "cost": {"shipping": "5.00", "insurance": "1.00"},
            "remarks": "Shipped via USPS",
        }
        result = bricklink_client.order.update_order(12345678, update_data)

        # Verify request was made correctly
        mock_oauth_session.put.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678",
            params=None,
            json=update_data,
        )

        # Verify response was processed correctly
        assert result["order_id"] == 12345678
        assert result["status"] == "UPDATED"

    def test_update_order_status(self, bricklink_client, mock_oauth_session):
        """Test updating order status."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"order_id": 12345678, "status": "SHIPPING"},
        }
        mock_oauth_session.put.return_value = mock_response

        # Call method
        status_data = {"field": "status", "value": "SHIPPING"}
        result = bricklink_client.order.update_order_status(12345678, status_data)

        # Verify request was made correctly
        mock_oauth_session.put.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678/status",
            params=None,
            json=status_data,
        )

        # Verify response was processed correctly
        assert result["order_id"] == 12345678
        assert result["status"] == "SHIPPING"

    def test_update_payment_status(self, bricklink_client, mock_oauth_session):
        """Test updating payment status."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"order_id": 12345678, "payment_status": "Received"},
        }
        mock_oauth_session.put.return_value = mock_response

        # Call method
        payment_data = {"field": "payment_status", "value": "Received"}
        result = bricklink_client.order.update_payment_status(12345678, payment_data)

        # Verify request was made correctly
        mock_oauth_session.put.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678/payment_status",
            params=None,
            json=payment_data,
        )

        # Verify response was processed correctly
        assert result["order_id"] == 12345678
        assert result["payment_status"] == "Received"

    def test_send_drive_thru(self, bricklink_client, mock_oauth_session):
        """Test sending drive thru email."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "data": {"success": True},
        }
        mock_oauth_session.put.return_value = mock_response

        # Call method
        result = bricklink_client.order.send_drive_thru(12345678, mail_me=True)

        # Verify request was made correctly
        mock_oauth_session.put.assert_called_once_with(
            "https://api.bricklink.com/api/store/v1/orders/12345678/drive_thru",
            params={"mail_me": True},
            json=None,
        )

        # Verify response was processed correctly
        assert result["success"] is True
