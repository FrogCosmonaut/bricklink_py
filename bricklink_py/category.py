from .utils import BaseResource


class Category(BaseResource):

    def get_category_list(self):
        """Retrieves a list of the categories defined within
        BrickLink catalog.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "categories"
        return self._request("get", uri)

    def get_category(self, category_id: int):
        """Retrieves information about a specific category.

        Arguments:
            category_id -- The ID of the category to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"categories/{category_id}"
        return self._request("get", uri)
