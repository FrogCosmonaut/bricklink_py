from .utils import BaseResource


class Feedback(BaseResource):

    def get_feedback_list(self, direction: str = "in"):
        """Gets a list of feedback you received or posted.

        Keyword Arguments:
            direction -- The direction of the feedback to get.
            (default: {in})
                Acceptable values are:
                "out": Gets posted feedback.
                "in": Gets received feedback.

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"direction": direction}
        uri = "feedback"
        return self._request("get", uri, params)

    def get_feedback(self, feedback_id: int):
        """Gets a specified feedback.

        Arguments:
            feedback_id -- The ID of the feedback to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"feedback/{feedback_id}"
        return self._request("get", uri)

    def post_feedback(self, body: dict):
        """Posts a new feedback about the transaction.

        Arguments:
            body -- In the request body, supply feedback resource.
                The feedback resource object should include:
                order_id, rating and comment

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "feedback"
        return self._request("post", uri, body=body)

    def reply_feedback(self, feedback_id: int, body: dict):
        """Creates a reply to the specified feedback you received.

        Arguments:
            feedback_id -- The ID of the feedback to post a reply.

            body -- In the request body, supply feedback resource.
                The feedback resource object should include: reply

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"feedback/{feedback_id}/reply"
        return self._request("post", uri, body=body)
