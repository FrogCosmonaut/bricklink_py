from .utils import BaseResource


class Setting(BaseResource):

    def get_shipping_methods(self):
        """Retrieves a list of shipping method you registered.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "settings/shipping_methods"
        return self._request("get", uri)

    def get_shipping_method(self, method_id: int):
        """Retrieves the specified shipping method of your store.

        Arguments:
            method_id -- The ID of the shipping method to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"settings/shipping_methods/{method_id}"
        return self._request("get", uri)
