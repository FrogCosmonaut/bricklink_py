from .utils import BaseResource


class Order(BaseResource):

    def get_orders(
        self, direction: str = "in", status: str = None, filed: bool = False
    ):
        """This method retrieves a list of orders you received or placed.

        Keyword Arguments:
            direction -- The direction of the order to get. (default: {in})
                "out": Gets placed orders.
                "in": Gets received orders.

            status -- The status of the order. (default: {None})
                If you don't specify this value, this method retrieves orders
                in any status.

                You can pass a comma-separated string to specify multiple
                status to include/exclude.

                You can add a minus(-) sign to specify a status to exclude

            filed -- Indicates whether the result retries filedorun-filed
            orders. (default: {False})

        Returns:
            A list of the the summary of an order resource as "data" in the
            response body.
        """
        params = {"direction": direction, "status": status, "filed": filed}
        uri = "orders"
        return self._request("get", uri, params)

    def get_order(self, order_id: int):
        """Retrieves the details of a specific order.

        Arguments:
            order_id -- The ID of the order to get

        Returns:
            An order resource as "data" in the response body.
        """
        uri = f"orders/{order_id}"
        return self._request("get", uri)

    def get_order_items(self, order_id: int):
        """Retrieves a list of items for the specified order.

        Arguments:
            order_id -- The ID of the order

        Returns:
            A list of items batch list as "data" in the response body.
            An inner list indicates items included in one batch of the order
            (order item batch).
        """
        uri = f"orders/{order_id}/items"
        return self._request("get", uri)

    def get_order_messages(self, order_id: int):
        """Retrieves a list of messages for the specified order that the user
        receives as a seller.

        Arguments:
            order_id -- The ID of the order

        Returns:
            A list of order message resource as "data" in the response body.
        """
        uri = f"orders/{order_id}/messages"
        return self._request("get", uri)

    def get_order_feedback(self, order_id: int):
        """Retrieves a list of feedback for the specified order.

        Arguments:
            order_id -- The ID of the order

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"orders/{order_id}/feedback"
        return self._request("get", uri)

    def update_order(self, order_id: int, body: dict):
        """Updates properties of a specific order.

        Arguments:
            order_id -- The ID of the order to update

            Body dictionary:\n
            ```
            {
            "shipping": {
                "date_shipped": "Timestamp",
                "tracking_no": "String",
                "tracking_link": "String",
                "method_id": "Integer"
            },
            "cost": {
                "shipping": "String",
                "insurance": "String",
                "credit": "String",
                "etc1": "String",
                "etc2": "String"
            },
            "is_filed" : "Boolean",
            "remarks" : "String"
            }
            ```
        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"orders/{order_id}"
        return self._request("put", uri, body=body)

    def update_order_status(self, order_id: int, body: dict):
        """Updates the status of a specific order.

        Arguments:
            order_id -- The ID of the order to update status

            Body dictionary:\n
            ```
            {
                "field" : "status",
                "value" : "PENDING"
            }
            ```
            Available status for value:
            https://www.bricklink.com/help.asp?helpID=41

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"orders/{order_id}/status"
        return self._request("put", uri, body=body)

    def update_payment_status(self, order_id: int, body: dict):
        """Updates the payment status of a specific order.

        Arguments:
            order_id -- The ID of the order to update payment status

            Body dictionary:\n
            ```
            {
                "field" : "payment_status",
                "value" : "Received"
            }
            ```
            Available status for value:
            https://www.bricklink.com/help.asp?helpID=121

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"orders/{order_id}/payment_status"
        return self._request("put", uri, body=body)

    def send_drive_thru(self, order_id: int, mail_me: bool = False):
        """Send "Thank You, Drive Thru!" e-mail to a buyer.

        Arguments:
            order_id -- The ID of the order to update payment status

        Keyword Arguments:
            mail_me -- Indicates that whether you want to cc yourself or not
            (default: {False})

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"mail_me": mail_me}
        uri = f"orders/{order_id}/drive_thru"
        return self._request("put", uri, params)
