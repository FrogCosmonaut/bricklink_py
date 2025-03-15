from .color import Color

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from .utils import BaseResource


class ItemType(Enum):
    """Valid item types in BrickLink catalog."""

    MINIFIG = "MINIFIG"
    PART = "PART"
    SET = "SET"
    BOOK = "BOOK"
    GEAR = "GEAR"
    CATALOG = "CATALOG"
    INSTRUCTION = "INSTRUCTION"
    UNSORTED_LOT = "UNSORTED_LOT"
    ORIGINAL_BOX = "ORIGINAL_BOX"


class GuideType(Enum):
    """Valid price guide types."""

    SOLD = "sold"  # Gets the price statistics of "Last 6 Months Sales"
    STOCK = "stock"  # Gets the price statistics of "Current Items for Sale"


class Condition(Enum):
    """Item condition values."""

    NEW = "N"
    USED = "U"


class Region(Enum):
    """Valid regions for price guides."""

    ASIA = "asia"
    AFRICA = "africa"
    NORTH_AMERICA = "north_america"
    SOUTH_AMERICA = "south_america"
    MIDDLE_EAST = "middle_east"
    EUROPE = "europe"
    EU = "eu"
    OCEANIA = "oceania"


class VatOption(Enum):
    """VAT inclusion options."""

    EXCLUDE = "N"
    INCLUDE = "Y"
    NORWAY = "O"  # Include VAT as Norway settings


class Item:
    """Represents a BrickLink catalog item."""

    def __init__(
        self, client, type: Union[ItemType, str], no: str, data: Dict[str, Any]
    ):
        """Initialize an item with its data and a reference to the client.

        Args:
            client: The CatalogItem client instance
            type: The type of the item
            no: Identification number of the item
            data: The item data from the API
        """
        self._client = client
        self.type = type.value if isinstance(type, ItemType) else type
        self.no = no

        for key, value in data.items():
            setattr(self, key, value)

    def get_image(self, color_id: Optional[int] = 0) -> Dict[str, str]:
        """Returns image URL of this item by colors."""
        return self._client.get_item_image(self.type, self.no, color_id)

    def get_supersets(self, color_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns a list of items that include this item."""
        return self._client.get_supersets(self.type, self.no, color_id)

    def get_subsets(
        self,
        color_id: Optional[int] = None,
        box: bool = False,
        instruction: bool = False,
        break_minifigs: bool = False,
        break_subsets: bool = False,
    ) -> List[Dict[str, Any]]:
        """Returns a list of items that are included in this item."""
        return self._client.get_subsets(
            self.type,
            self.no,
            color_id,
            box,
            instruction,
            break_minifigs,
            break_subsets,
        )

    def get_price_guide(
        self,
        color_id: Optional[int] = None,
        guide_type: Union[GuideType, str] = GuideType.STOCK,
        new_or_used: Union[Condition, str] = Condition.NEW,
        country_code: Optional[str] = None,
        region: Optional[Union[Region, str]] = None,
        currency_code: Optional[str] = None,
        vat: Union[VatOption, str] = VatOption.EXCLUDE,
    ) -> Dict[str, Any]:
        """Returns the price statistics of this item."""
        return self._client.get_price_guide(
            self.type,
            self.no,
            color_id,
            guide_type,
            new_or_used,
            country_code,
            region,
            currency_code,
            vat,
        )

    def get_known_colors(self) -> List[Dict[str, Any]]:
        """Returns currently known colors of this item."""
        return self._client.get_known_colors(self.type, self.no)

    def __str__(self) -> str:
        """String representation of the item."""
        return f"Item({self.type}, {self.no})"

    def __repr__(self) -> str:
        """Detailed representation of the item."""
        return f"Item(type={self.type}, no={self.no}, data={self._data})"


class CatalogItem(BaseResource):
    """Client for BrickLink catalog item operations."""

    def get_item(self, type: Union[ItemType, str], no: str) -> Item:
        """Returns information about the specified item in BrickLink catalog.

        Args:
            type: The type of the item to get.
            no: Identification number of the item to get.

        Returns:
            An Item object containing the item information.

        Raises:
            ValueError: If item number is not provided.
            requests.RequestException: If the API request fails.
        """
        if not no:
            raise ValueError("Item number not provided")

        item_type = type.value if isinstance(type, ItemType) else type

        uri = f"items/{item_type}/{no}"
        data = self._request("get", uri)

        # Create an Item instance with the API response data
        return Item(self, type, no, data)

    def get_item_image(
        self, type: Union[ItemType, str], no: str, color_id: Optional[int] = 0
    ) -> Dict[str, str]:
        """Returns image URL of the specified item by colors.

        Args:
            type: The type of the item to get.
            no: Identification number of the item to get.
            color_id: The color ID of the item.

        Returns:
            Dict containing the image URL.

        Raises:
            requests.RequestException: If the API request fails.
        """
        if not no:
            raise ValueError("Item number not provided")

        item_type = type.value if isinstance(type, ItemType) else type

        uri = f"items/{item_type}/{no}/images/{color_id}"
        return self._request("get", uri)

    def get_supersets(
        self, type: Union[ItemType, str], no: str, color_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Returns a list of items that include the specified item.

        Args:
            type: The type of the item to get.
            no: Identification number of the item to get.
            color_id: The color of the item. Optional.

        Returns:
            List of dicts containing the superset items.

        Raises:
            requests.RequestException: If the API request fails.
        """
        if not no:
            raise ValueError("Item number not provided")

        item_type = type.value if isinstance(type, ItemType) else type

        params = {"color_id": color_id} if color_id else {}
        uri = f"items/{item_type}/{no}/supersets"
        return self._request("get", uri, params)

    def get_subsets(
        self,
        type: Union[ItemType, str],
        no: str,
        color_id: Optional[int] = None,
        box: bool = False,
        instruction: bool = False,
        break_minifigs: bool = False,
        break_subsets: bool = False,
    ) -> List[Dict[str, Any]]:
        """Returns a list of items that are included in the specified item.

        Args:
            type: The type of the item to get.
            no: Identification number of the item to get.
            color_id: The color of the item. Only valid for PART type.
            box: Whether the set includes the original box.
            instruction: Whether the set includes the original instruction.
            break_minifigs: Whether the result breaks down minifigs as parts.
            break_subsets: Whether the result breaks down sets in set.

        Returns:
            List of dicts containing the subset items.

        Raises:
            requests.RequestException: If the API request fails.
        """
        if not no:
            raise ValueError("Item number not provided")

        item_type = type.value if isinstance(type, ItemType) else type

        params = {
            "color_id": color_id,
            "box": str(box).lower(),
            "instruction": str(instruction).lower(),
            "break_minifigs": str(break_minifigs).lower(),
            "break_subsets": str(break_subsets).lower(),
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        uri = f"items/{item_type}/{no}/subsets"
        return self._request("get", uri, params)

    def get_price_guide(
        self,
        type: Union[ItemType, str],
        no: str,
        color_id: Optional[int] = None,
        guide_type: Union[GuideType, str] = GuideType.STOCK,
        new_or_used: Union[Condition, str] = Condition.NEW,
        country_code: Optional[str] = None,
        region: Optional[Union[Region, str]] = None,
        currency_code: Optional[str] = None,
        vat: Union[VatOption, str] = VatOption.EXCLUDE,
    ) -> Dict[str, Any]:
        """Returns the price statistics of the specified item.

        Args:
            type: The type of the item to get.
            no: Identification number of the item to get.
            color_id: The color of the item.
            guide_type: Which statistics to provide ('sold' or 'stock').
            new_or_used: The condition of items ('N' for new, 'U' for used).
            country_code: Filter by country code.
            region: Filter by region.
            currency_code: Currency for prices.
            vat: VAT inclusion option.

        Returns:
            Dict containing price guide information.

        Raises:
            requests.RequestException: If the API request fails.
        """
        if not no:
            raise ValueError("Item number not provided")

        item_type = type.value if isinstance(type, ItemType) else type
        guide_type_val = (
            guide_type.value if isinstance(guide_type, GuideType) else guide_type
        )
        condition_val = (
            new_or_used.value if isinstance(new_or_used, Condition) else new_or_used
        )
        region_val = region.value if isinstance(region, Region) else region
        vat_val = vat.value if isinstance(vat, VatOption) else vat

        params = {
            "color_id": color_id,
            "guide_type": guide_type_val,
            "new_or_used": condition_val,
            "country_code": country_code,
            "region": region_val,
            "currency_code": currency_code,
            "vat": vat_val,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        uri = f"items/{item_type}/{no}/price"
        return self._request("get", uri, params)

    def get_known_colors(
        self, type: Union[ItemType, str], no: str
    ) -> List[Dict[str, Any]]:
        """Returns currently known colors of the item.

        Args:
            type: The type of the item to get.
            no: Identification number of the item to get.

        Returns:
            List of dicts containing color information.

        Raises:
            requests.RequestException: If the API request fails.
        """
        if not no:
            raise ValueError("Item number not provided")

        item_type = type.value if isinstance(type, ItemType) else type

        uri = f"items/{item_type}/{no}/colors"
        colors = self._request("get", uri)
        return [Color(*c) for c in colors]
