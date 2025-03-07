from .utils import BaseResource


class PushNotification(BaseResource):

    def get_notifications(self):
        """Returns a list of unread push notifications. If you provided
        callback URLs to get notifications, you don't need to call this
        method.

        A notification to be created when:
        - You received a new order.
        - Buyer updates an order status.
        - Items of an order are updated (added or deleted).
        - You received a new message.
        - You received a new feedback or reply.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "notifications"
        return self._request("get", uri)
