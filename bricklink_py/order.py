from .utils import BaseResource

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class BricklinkOrderPayment:
    method: str
    currency_code: str
    date_paid: datetime
    status: str

    def __post_init__(self):
        if isinstance(self.date_paid, str):
            self.date_paid = datetime.fromisoformat(self.date_paid)


@dataclass
class BricklinkShipping:
    method_id: int
    method: str
    tracking_link: str
    address: dict
    full: str
    country_code: str


@dataclass
class BricklinkOrderCost:
    currency_code: str
    subtotal: float = 0.0
    grand_total: float = 0.0
    final_total: float = 0.0
    etc1: float = 0.0
    etc2: float = 0.0
    insurance: float = 0.0
    shipping: float = 0.0
    credit: float = 0.0
    coupon: float = 0.0
    vat_rate: float = 0.0
    vat_amount: float = 0.0
    salesTax_collected_by_bl: str = None

    def __post_init__(self):
        self.subtotal = float(self.subtotal)
        self.grand_total = float(self.grand_total)
        self.final_total = float(self.final_total)
        self.etc1 = float(self.etc1)
        self.etc2 = float(self.etc2)
        self.insurance = float(self.insurance)
        self.shipping = float(self.shipping)
        self.credit = float(self.credit)
        self.coupon = float(self.coupon)
        self.vat_rate = float(self.vat_rate)
        self.vat_rate = float(self.vat_rate)


@dataclass
class BricklinkOrderDispCost(BricklinkOrderCost):
    pass


class OrderManager(BaseResource):
    """Manager class for Bricklink orders that handles API operations"""

    def get_orders(
        self,
        direction: str = "in",
        status: str = None,
        filed: bool = False,
    ) -> List["BricklinkOrder"]:
        """This method retrieves a list of orders you received or placed.

        Keyword Arguments:
            direction -- The direction of the order to get. (default: {in})
                "out": Gets placed orders.
                "in": Gets received orders.

            status -- The status of the order. (default: {None})
                If you don't specify this value, this method retrieves orders
                in any status.

                You can pass a comma-separated string to specify multiple
                status to include/exclude.

                You can add a minus(-) sign to specify a status to exclude

            filed -- Indicates whether the result retries filed or unfiled
            orders. (default: {False})

        Returns:
            A list of BricklinkOrder objects.
        """
        params = {"direction": direction, "status": status, "filed": filed}
        uri = "orders"
        orders = self._request("get", uri, params)
        return [BricklinkOrder.from_dict(o, self) for o in orders]

    def get_order(self, order_id: int) -> "BricklinkOrder":
        """Retrieves the details of a specific order.

        Arguments:
            order_id -- The ID of the order to get

        Returns:
            A BricklinkOrder object.
        """
        uri = f"orders/{order_id}"
        order_data = self._request("get", uri)
        return BricklinkOrder.from_dict(order_data, self)


@dataclass
class BricklinkOrder:
    order_id: int
    date_ordered: datetime
    date_status_changed: datetime
    seller_name: str = None
    store_name: str = None
    buyer_name: str = None
    buyer_email: str = None
    require_insurance: bool = None
    status: str = None
    is_invoiced: bool = None
    remarks: str = None
    total_count: int = None
    unique_count: int = None
    total_weight: float = None
    buyer_order_count: int = None
    is_filed: bool = None
    salesTax_collected_by_bl: bool = None
    vat_collected_by_bl: bool = None
    payment: BricklinkOrderPayment = None
    cost: BricklinkOrderCost = None
    disp_cost: BricklinkOrderDispCost = None
    _manager: Optional[OrderManager] = None  # Reference to the API manager

    def __post_init__(self):
        if isinstance(self.date_ordered, str):
            self.date_ordered = datetime.fromisoformat(self.date_ordered)
        if isinstance(self.date_status_changed, str):
            self.date_status_changed = datetime.fromisoformat(self.date_status_changed)

    @classmethod
    def from_dict(
        cls, data: dict, manager: Optional[OrderManager] = None
    ) -> "BricklinkOrder":
        """Create a BricklinkOrder from a dictionary representation"""
        d_copy = data.copy()
        payment = d_copy.pop("payment")
        cost = d_copy.pop("cost")
        disp_cost = d_copy.pop("disp_cost")
        return cls(
            **d_copy,
            payment=BricklinkOrderPayment(**payment),
            cost=BricklinkOrderCost(**cost),
            disp_cost=BricklinkOrderDispCost(**disp_cost),
            _manager=manager,
        )

    def get_items(self) -> List[Dict[str, Any]]:
        """Retrieves a list of items for this order.

        Returns:
            A list of items batch list.
            An inner list indicates items included in one batch of the order
            (order item batch).
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        uri = f"orders/{self.order_id}/items"
        return self._manager._request("get", uri)

    def get_messages(self) -> List[Dict[str, Any]]:
        """Retrieves a list of messages for this order that the user
        receives as a seller.

        Returns:
            A list of order message resources.
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        uri = f"orders/{self.order_id}/messages"
        return self._manager._request("get", uri)

    def get_feedback(self) -> List[Dict[str, Any]]:
        """Retrieves a list of feedback for this order.

        Returns:
            A list of feedback resources.
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        uri = f"orders/{self.order_id}/feedback"
        return self._manager._request("get", uri)

    def update(
        self,
        shipping: Optional[Dict[str, Any]] = None,
        cost: Optional[Dict[str, Any]] = None,
        is_filed: Optional[bool] = None,
        remarks: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates properties of this order.

        Keyword Arguments:
            shipping -- Dictionary containing shipping information
                {
                    "date_shipped": "Timestamp",
                    "tracking_no": "String",
                    "tracking_link": "String",
                    "method_id": "Integer"
                }
            cost -- Dictionary containing cost information
                {
                    "shipping": "String",
                    "insurance": "String",
                    "credit": "String",
                    "etc1": "String",
                    "etc2": "String"
                }
            is_filed -- Boolean indicating if the order is filed
            remarks -- String with remarks about the order

        Returns:
            Response data from the API.
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        # Build the update body
        body = {}
        if shipping is not None:
            body["shipping"] = shipping
        if cost is not None:
            body["cost"] = cost
        if is_filed is not None:
            body["is_filed"] = is_filed
        if remarks is not None:
            body["remarks"] = remarks

        uri = f"orders/{self.order_id}"
        response = self._manager._request("put", uri, body=body)

        return response

    def update_status(self, status: str) -> Dict[str, Any]:
        """Updates the status of this order.

        Arguments:
            status -- The new status for the order

            Available status values:
            https://www.bricklink.com/help.asp?helpID=41

        Returns:
            Response data from the API.
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        body = {"field": "status", "value": status}
        uri = f"orders/{self.order_id}/status"
        response = self._manager._request("put", uri, body=body)

        self.status = status

        return response

    def update_payment_status(self, payment_status: str) -> Dict[str, Any]:
        """Updates the payment status of this order.

        Arguments:
            payment_status -- The new payment status

            Available status values:
            https://www.bricklink.com/help.asp?helpID=121

        Returns:
            Response data from the API.
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        body = {"field": "payment_status", "value": payment_status}
        uri = f"orders/{self.order_id}/payment_status"
        response = self._manager._request("put", uri, body=body)

        return response

    def send_drive_thru(self, mail_me: bool = False) -> Dict[str, Any]:
        """Send "Thank You, Drive Thru!" e-mail to a buyer.

        Keyword Arguments:
            mail_me -- Indicates that whether you want to cc yourself or not
            (default: {False})

        Returns:
            Response data from the API.
        """
        if not self._manager:
            raise ValueError("This order is not associated with an API manager")

        params = {"mail_me": mail_me}
        uri = f"orders/{self.order_id}/drive_thru"
        return self._manager._request("post", uri, params)
