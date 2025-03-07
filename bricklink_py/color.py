from .utils import BaseResource


class Color(BaseResource):

    def get_color_list(self):
        """Retrieves a list of the colors defined within BrickLink catalog.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "colors"
        return self._request("get", uri)

    def get_color(self, color_id: int):
        """Retrieves information about a specific color.

        Arguments:
            color_id -- The ID of the color to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"colors/{color_id}"
        return self._request("get", uri)
