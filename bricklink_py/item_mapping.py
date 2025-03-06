from .utils import BaseResource


class ItemMapping(BaseResource):

    def get_element_id(self, type: str, no: str, color_id: int = None):
        """Returns Part-Color-Code (A.K.A ElementID) of the specified item.

        Arguments:
            type -- The type of an item to get. Acceptable values are: PART

            no -- Identification number of an item to get.

        Keyword Arguments:
            color_id -- Color ID of an item. If not specified, API retrieves
            element IDs of an item in any colors. (default: {None})

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"color_id": color_id}
        uri = f"item_mapping/{type}/{no}"
        return self._request("get", uri, params)

    def get_item_number(self, element_id: str):
        """Returns BL Catalog Item Number by Part-Color-Code (A.K.A ElementID)

        Arguments:
            element_id -- Element ID of the item in specific color.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"item_mapping/{element_id}"
        return self._request("get", uri)
