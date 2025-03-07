from requests_oauthlib import OAuth1Session

from .catalog_item import CatalogItem
from .category import Category
from .color import Color
from .coupon import Coupon
from .feedback import Feedback
from .item_mapping import ItemMapping
from .member import Member
from .order import Order
from .push_notification import PushNotification
from .setting import Setting
from .store_inventory import StoreInventory


class Bricklink:
    """Main client for the Bricklink API."""

    def __init__(
        self,
        consumer_key: str = None,
        consumer_secret: str = None,
        token: str = None,
        token_secret: str = None,
    ):
        """
        Initialize the Bricklink API client

        Arguments:
            consumer_key: OAuth consumer key
            consumer_secret: OAuth consumer secret
            token: OAuth token
            token_secret: OAuth token secret
        """
        self.oauth_session = self._authenticate(
            consumer_key, consumer_secret, token, token_secret
        )

        self.order = Order(self.oauth_session)
        self.store_inventory = StoreInventory(self.oauth_session)
        self.catalog_item = CatalogItem(self.oauth_session)
        self.feedback = Feedback(self.oauth_session)
        self.color = Color(self.oauth_session)
        self.category = Category(self.oauth_session)
        self.push_notification = PushNotification(self.oauth_session)
        self.coupon = Coupon(self.oauth_session)
        self.setting = Setting(self.oauth_session)
        self.member = Member(self.oauth_session)
        self.item_mapping = ItemMapping(self.oauth_session)

    def _authenticate(self, ck: str, cs: str, tk: str, tks: str) -> OAuth1Session:
        """
        Create authenticated OAuth session

        Arguments:
            ck: Consumer key
            cs: Consumer secret
            tk: Token
            tks: Token secret

        Returns:
            Authenticated OAuth1Session
        """
        return OAuth1Session(
            client_key=ck,
            client_secret=cs,
            resource_owner_key=tk,
            resource_owner_secret=tks,
        )
