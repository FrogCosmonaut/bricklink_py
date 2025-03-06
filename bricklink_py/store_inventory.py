from .utils import BaseResource


class StoreInventory(BaseResource):

    def get_store_inventories(
        self,
        item_type: str = None,
        status: str = None,
        category_id: int = None,
        color_id: int = None,
    ):
        """Retrieves a list of inventories you have.

        Keyword Arguments:
            item_type -- The type of the item to include or exclude.
            (default: {None})
                If you don't specify this value, this method retrieves
                inventories with any type of item.

                You can pass a comma-separated string to specify multiple item
                types to include/exclude.

                You can add a minus( - ) sign to specify a type to exclude.

            status -- The status of the inventory to include or exclude.
            (default: {None})
                Available values are:

                "Y" : available
                "S" : in stockroom A
                "B" : in stockroom B
                "C" : in stockroom C
                "N" : unavailable
                "R" : reserved

                If you don't specify this value, this method retrieves
                inventories in any status.

                You can pass a comma-separated string to specify multiple
                status to include/exclude.

                You can add a minus( - ) sign to specify a status to exclude.

            category_id -- The ID of the category to include or exclude.
            (default: {None})
                If you don't specify this value, this method retrieves
                inventories with any category of item.

                You can pass a comma-separated string to specify multiple
                categories to include/exclude.

                You can add a minus(-) sign to specify a category to exclude.

                You can only specify the main category of the item.

            color_id -- The ID of the color to include or exclude
            (default: {None})
                If you don't specify this value, this method retrieves
                inventories with any color of item.

                You can pass a comma-separated string to specify multiple
                colors to include/exclude.

                You can add a minus(-) sign to specify a color to exclude.

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {
            "item_type": item_type,
            "status": status,
            "category_id": category_id,
            "color_id": color_id,
        }
        uri = "inventories"
        return self._request("get", uri, params)

    def get_store_inventory(self, inventory_id: int):
        """Retrieves information about a specific inventory.

        Arguments:
            inventory_id -- The ID of the inventory to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"inventories/{inventory_id}"
        return self._request("get", uri)

    def create_store_inventory(self, body: dict):
        """Creates a new inventory with an item.

        Arguments:
            body -- Supply a store inventory resource. The store inventory
            resource should include:

            {item.no}, {item.type}, {color_id}, {quantity}, {unit_price},
            {new_or_used}, {completeness} (only when item.type is "set"),
            {description}, {remarks}, {bulk}, {is_retain}, {is_stock_room},
            {stock_room_id} (only when is_stock_room is "true"), {my_cost},
            {sale_rate}, {tier_quantity1}, {tier_price1}, {tier_quantity2},
            {tier_price2}, {tier_quantity3}, {tier_price3}

            Note that to set tier price options, all 6 values must be entered

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "inventories"
        return self._request("post", uri, body=body)

    def create_store_inventories(self, body: dict):
        """Creates multiple inventories in a single request. Note that you can
        create an inventory only with items in the BL Catalog.

        Arguments:
            body -- Supply a store inventory resource. The store inventory
            resource should include:

            {item.no}, {item.type}, {color_id}, {quantity}, {unit_price},
            {new_or_used}, {completeness} (only when item.type is "set"),
            {description}, {remarks}, {bulk}, {is_retain}, {is_stock_room},
            {stock_room_id} (only when is_stock_room is "true"), {my_cost},
            {sale_rate}, {tier_quantity1}, {tier_price1}, {tier_quantity2},
            {tier_price2}, {tier_quantity3}, {tier_price3}

            Note that to set tier price options, all 6 values must be entered

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "inventories"
        return self._request("post", uri, body=body)

    def update_store_inventory(self, inventory_id: int, body: dict):
        """Updates properties of the specified inventory.

        Arguments:
            inventory_id -- The ID of the inventory to update.

            body -- Supply a store inventory resource. The store inventory
            resource should include:
                {+quantity}, {unit_price}, {description}, {remarks}, {bulk},
                {is_retain}, {is_stock_room},
                {stock_room_id} (only when is_stock_room is "true"),
                {my_cost}, {sale_rate}, {tier_quantity1}, {tier_price1},
                {tier_quantity2}, {tier_price2}, {tier_quantity3},
                {tier_price3}

                Note that to set tier price options, all 6 values must be entered

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"inventories/{inventory_id}"
        return self._request("put", uri, body=body)

    def delete_store_inventory(self, inventory_id: int):
        """Deletes the specified inventory.

        Arguments:
            inventory_id -- The ID of the inventory to delete.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"inventories/{inventory_id}"
        return self._request("delete", uri)
