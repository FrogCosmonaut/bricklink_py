from .utils import BaseResource


class Coupon(BaseResource):

    def get_coupons(self, direction: str = "out", status: str = None):
        """Retrieves a list of coupons you received or created.

        Keyword Arguments:
            direction -- The direction of the coupon to get. (default: {out})
                Acceptable values are:

                "out": Gets created coupons, "in": Gets received coupons

            status -- The status of the store inventory to include or exclude.
            (default: {None})
                Available values are:

                "O" : open

                "S" : redeemed

                "D" : denied

                "E" : expired

                If you don't specify this value, this method retrieves coupons
                in any status.

                You can pass a comma-separated string to specify multiple
                status to include/exclude.

                You can add a minus(-) sign to specify a status to exclude.

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"direction": direction, "status": status}
        uri = "coupons"
        return self._request("get", uri, params)

    def get_coupon(self, coupon_id: int):
        """Retrieves a specific coupon.

        Arguments:
            coupon_id -- The ID of the coupon to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"coupons/{coupon_id}"
        return self._request("get", uri)

    def create_coupon(self, body: dict):
        """Creates a new coupon for a buyer.

        Arguments:
            body -- Supply a coupon resource.
            https://www.bricklink.com/v3/api.page?page=resource-representations-coupon

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "coupons"
        return self._request("post", uri, body=body)

    def update_coupon(self, coupon_id: int, body: dict):
        """Updates properties of the specified coupon.

        Arguments:
            coupon_id -- The ID of the coupon to update.

            body -- Supply a coupon resource.
        https://www.bricklink.com/v3/api.page?page=resource-representations-coupon

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"coupons/{coupon_id}"
        return self._request("put", uri, body=body)

    def delete_coupon(self, coupon_id):
        """Deletes the specified coupon.

        Arguments:
            coupon_id -- The ID of the coupon to delete.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"coupons/{coupon_id}"
        return self._request("delete", uri)
