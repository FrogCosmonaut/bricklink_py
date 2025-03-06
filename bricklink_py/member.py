from .utils import BaseResource


class Member(BaseResource):

    def get_member_rating(self, username: str):
        """Retrieves feedback ratings of a specific member.

        Arguments:
            username -- username in BrickLink.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"members/{username}/ratings"
        return self._request("get", uri)

    def get_member_note(self, username: str):
        """Retrieves your notes on a member.

        Arguments:
            username -- username in BrickLink.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"members/{username}/notes"
        return self._request("get", uri)

    def create_member_note(self, username: str, body: dict):
        """_summary_

        Arguments:
            username -- username in BrickLink.

            body -- Note resource:
        https://www.bricklink.com/v3/api.page?page=resource-representations-member

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"members/{username}/notes"
        return self._request("post", uri, body=body)

    def update_member_note(self, username: str, body: dict):
        """Updates properties of your member notes on the specified user.

        Arguments:
            username -- username in BrickLink.

            body -- Note resource:
        https://www.bricklink.com/v3/api.page?page=resource-representations-member

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"members/{username}/notes"
        return self._request("put", uri, body=body)

    def delete_member_note(self, username: str):
        """Deletes the notes on the specified user.

        Arguments:
            username -- username in BrickLink.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"members/{username}/notes"
        return self._request("delete", uri)
