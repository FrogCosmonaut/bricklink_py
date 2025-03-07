from .utils import BaseResource


class CatalogItem(BaseResource):

    def get_item(self, type: str, no: str):
        """Returns information about the specified item in BrickLink catalog.

        Arguments:
            type -- The type of the item to get. Acceptable values are:
                MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION,
                UNSORTED_LOT, ORIGINAL_BOX

            no -- Identification number of the item to get

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"items/{type}/{no}"
        return self._request("get", uri)

    def get_item_image(self, type: str, no: str, color_id: int):
        """Returns image URL of the specified item by colors.

        Arguments:
            type -- The type of the item to get. Acceptable values are:
                MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION,
                UNSORTED_LOT, ORIGINAL_BOX

            no -- Identification number of the item to get.

            color_id -- The color of the item.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"items/{type}/{no}/images/{color_id}"
        return self._request("get", uri)

    def get_supersets(self, type: str, no: str, color_id: int = None):
        """Returns a list of items that include the specified item.

        Arguments:
            type -- The type of the item to get. Acceptable values are:
                MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION,
                UNSORTED_LOT, ORIGINAL_BOX

            no -- Identification number of the item to get.

        Keyword Arguments:
            color_id -- The color of the item. (default: {None})

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"color_id": color_id}
        uri = f"items/{type}/{no}/supersets"
        return self._request("get", uri, params)

    def get_subsets(
        self,
        type: str,
        no: str,
        color_id: int = None,
        box: bool = False,
        instruction: bool = False,
        break_minifigs: bool = False,
        break_subsets: bool = False,
    ):
        """Returns a list of items that are included in the specified item.

        Arguments:
            type -- The type of the item to get. Acceptable values are:
                MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION,
                UNSORTED_LOT, ORIGINAL_BOX

            no -- Identification number of the item to get.

        Keyword Arguments:
            color_id -- The color of the item.
            (This value is valid only for PART type) (default: {None})

            box -- Indicates whether the set includes the original box.
            (default: {False})

            instruction -- Indicates whether the set includes the original
            instruction. (default: {False})

            break_minifigs -- Indicates whether the result breaks down
            minifigs as parts. (default: {False})

            break_subsets -- Indicates whether the result breaks down sets in
            set. (default: {False})

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {
            "color_id": color_id,
            "box": box,
            "instruction": instruction,
            "break_minifigs": break_minifigs,
            "break_subsets": break_subsets,
        }
        uri = f"items/{type}/{no}/subsets"
        return self._request("get", uri, params)

    def get_price_guide(
        self,
        type: str,
        no: str,
        color_id: int = None,
        guide_type: str = "stock",
        new_or_used: str = "N",
        country_code: str = None,
        region: str = None,
        currency_code: str = None,
        vat: str = "N",
    ):
        """Returns the price statistics of the specified item in
        BrickLink catalog.

        Arguments:
            type -- The type of the item to get. Acceptable values are:
                MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION,
                UNSORTED_LOT, ORIGINAL_BOX

            no -- Identification number of the item to get.

        Keyword Arguments:
            color_id -- The color of the item. (default: {None})

            guide_type -- Indicates that which statistics to be provided.
            (default: {stock})

                Acceptable values are:

                "sold": Gets the price statistics of "Last 6 Months Sales"

                "stock": Gets the price statistics of "Current Items for Sale"

            new_or_used -- Indicates the condition of items that are included
            in the statistics. (default: {N})

                Acceptable values are:
                "N": new item
                "U": used item

            country_code -- The result includes only items in stores which are
            located in specified country. (default: {None})

                If you don't specify both country_code and region, this method
                retrieves the price information regardless of the store's
                location.

            region -- The result includes only items in stores which are
            located in specified region. (default: {None})

                Available values are: asia, africa, north_america,
                south_america, middle_east, europe, eu, oceania

                If you don't specify both country_code and region, this method
                retrieves the price information regardless of the store's
                location.

            currency_code -- This method returns price in the specified
            currency code.(default: {None})

                If you don't specify this value, price is retrieved in the
                base currency of the user profile's.

            vat -- Indicates that price will include VAT for the items of VAT
            enabled stores. (default: {"N"})

                Available values are:
                "N": Exclude VAT
                "Y": Include VAT
                "O": Include VAT as Norway settings

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {
            "color_id": color_id,
            "guide_type": guide_type,
            "new_or_used": new_or_used,
            "country_code": country_code,
            "region": region,
            "currency_code": currency_code,
            "vat": vat,
        }
        uri = f"items/{type}/{no}/price"
        return self._request("get", uri, params)

    def get_known_colors(self, type: str, no: str):
        """Returns currently known colors of the item.

        Arguments:
            type -- The type of the item to get. Acceptable values are:
                MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION,
                UNSORTED_LOT, ORIGINAL_BOX

            no -- Identification number of the item to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"items/{type}/{no}/colors"
        return self._request("get", uri)
