from . import config

from .utils import request

from requests_oauthlib import OAuth1Session

class Bricklink():
    def __init__(self, consumer_key: str, consumer_secret: str,
                token: str, token_secret: str):
        self._oauth_session = OAuth1Session(
            client_key=str(consumer_key),
            client_secret=str(consumer_secret), 
            resource_owner_key=str(token),
            resource_owner_secret=str(token_secret))
        self.order = _Order(self._oauth_session)
        self.store_inventory = _StoreInventory(self._oauth_session)
        self.catalog_item = _CatalogItem(self._oauth_session)
        self.feedback = _Feedback(self._oauth_session)
        self.color = _Color(self._oauth_session)
        self.category = _Category(self._oauth_session)
        self.push_notification = _PushNotification(self._oauth_session)
        self.coupon = _Coupon(self._oauth_session)
        self.setting = _Setting(self._oauth_session)
        self.member = _Member(self._oauth_session)
        self.item_mapping = _ItemMapping(self._oauth_session)

    def _get_credentials(self):
        raise NotImplementedError('Not implemented.')

class _BaseResource:
    def __init__(self, oauth_session):
        self._oauth_session = oauth_session
        
class _Order(_BaseResource):
    def get_orders(self, direction: str = 'in',
                   status: str = None, filed: bool = False):
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

            filed -- Indicates whether the result retries filedorun-filed
            orders. (default: {False})

        Returns:
            A list of the the summary of an order resource as "data" in the
            response body.
        """
        params = {
            'direction': direction,
            'status': status,
            'filed': filed}
        uri = f'orders'
        return request('get', self._oauth_session, uri, params)
    
    def get_order(self, order_id: int):
        """Retrieves the details of a specific order.

        Arguments:
            order_id -- The ID of the order to get

        Returns:
            An order resource as "data" in the response body.
        """
        uri = f'orders/{order_id}'
        return request('get', self._oauth_session, uri)

    def get_order_items(self, order_id: int):
        """Retrieves a list of items for the specified order.

        Arguments:
            order_id -- The ID of the order

        Returns:
            A list of items batch list as "data" in the response body.
            An inner list indicates items included in one batch of the order
            (order item batch).
        """
        uri = f'orders/{order_id}/items'
        return request('get', self._oauth_session, uri)
    
    def get_order_messages(self, order_id: int):
        """Retrieves a list of messages for the specified order that the user
        receives as a seller.

        Arguments:
            order_id -- The ID of the order

        Returns:
            A list of order message resource as "data" in the response body.
        """
        uri = f'orders/{order_id}/messages'
        return request('get', self._oauth_session, uri)
    
    def get_order_feedback(self, order_id: int):
        """Retrieves a list of feedback for the specified order.

        Arguments:
            order_id -- The ID of the order

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'orders/{order_id}/feedback'
        return request('get', self._oauth_session, uri)
    
    def update_order(self, order_id: int, body: dict):
        """Updates properties of a specific order.

        Arguments:
            order_id -- The ID of the order to update

            Body dictionary:\n
            ```
            {
            "shipping": {
                "date_shipped": "Timestamp",
                "tracking_no": "String",
                "tracking_link": "String",
                "method_id": "Integer" 
            },
            "cost": {
                "shipping": "String",
                "insurance": "String",
                "credit": "String",
                "etc1": "String",
                "etc2": "String" 
            },
            "is_filed" : "Boolean",
            "remarks" : "String" 
            }
            ```
        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'orders/{order_id}'
        return request('put', self._oauth_session, uri, body=body)
    
    def update_order_status(self, order_id: int, body: dict):
        """Updates the status of a specific order.

        Arguments:
            order_id -- The ID of the order to update status

            Body dictionary:\n
            ```
            {
                "field" : "status",
                "value" : "PENDING"
            }
            ```
            Available status for value:
            https://www.bricklink.com/help.asp?helpID=41
            
        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'orders/{order_id}/status'
        return request('put', self._oauth_session, uri, body=body)

    def update_payment_status(self, order_id: int, body: dict):
        """Updates the payment status of a specific order.

        Arguments:
            order_id -- The ID of the order to update payment status

            Body dictionary:\n
            ```
            {
                "field" : "payment_status",
                "value" : "Received" 
            }
            ```
            Available status for value:
            https://www.bricklink.com/help.asp?helpID=121
            
        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'orders/{order_id}/payment_status'
        return request('put', self._oauth_session, uri, body=body)
    
    def send_drive_thru(self, order_id: int, mail_me: bool = False):
        """Send "Thank You, Drive Thru!" e-mail to a buyer.

        Arguments:
            order_id -- The ID of the order to update payment status

        Keyword Arguments:
            mail_me -- Indicates that whether you want to cc yourself or not
            (default: {False})

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"mail_me": mail_me}
        uri = f'orders/{order_id}/drive_thru'
        return request('put', self._oauth_session, uri, params)

class _StoreInventory(_BaseResource):
    def get_store_inventories(self, item_type: str = None, status: str = None,
                              category_id: int = None, color_id: int = None):
        """Retrieves a list of inventories you have.

        Keyword Arguments:
            item_type -- The type of the item to include or exclude.
            (default: {None})
                If you don't specify this value, this method retrieves
                inventories with any type of item.

                You can pass a comma-separated string to specify multiple item
                types to include/exclude.

                You can add a minus( - ) sign to specify a type to exclude.

            status -- The status of the inventory to include or exclude.
            (default: {None})
                Available values are:

                "Y" : available

                "S" : in stockroom A

                "B" : in stockroom B

                "C" : in stockroom C

                "N" : unavailable

                "R" : reserved

                If you don't specify this value, this method retrieves
                inventories in any status.

                You can pass a comma-separated string to specify multiple
                status to include/exclude.

                You can add a minus( - ) sign to specify a status to exclude.

            category_id -- The ID of the category to include or exclude.
            (default: {None})
                If you don't specify this value, this method retrieves
                inventories with any category of item.

                You can pass a comma-separated string to specify multiple
                categories to include/exclude.

                You can add a minus(-) sign to specify a category to exclude.

                You can only specify the main category of the item.

            color_id -- The ID of the color to include or exclude
            (default: {None})
                If you don't specify this value, this method retrieves
                inventories with any color of item.

                You can pass a comma-separated string to specify multiple
                colors to include/exclude.

                You can add a minus(-) sign to specify a color to exclude.

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {
            "item_type": item_type,
            "status": status,
            "category_id": category_id,
            "color_id": color_id
        }
        uri = f'inventories'
        return request('get', self._oauth_session, uri, params)
    
    def get_store_inventory(self, inventory_id: int):
        """Retrieves information about a specific inventory.

        Arguments:
            inventory_id -- The ID of the inventory to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'inventories/{inventory_id}'
        return request('get', self._oauth_session, uri)
    
    def create_store_inventory(self, body: dict):
        """Creates a new inventory with an item.

        Arguments:
            body -- Supply a store inventory resource. The store inventory
            resource should include:

            {item.no}, {item.type}, {color_id}, {quantity}, {unit_price},
            {new_or_used}, {completeness} (only when item.type is "set"),
            {description}, {remarks}, {bulk}, {is_retain}, {is_stock_room},
            {stock_room_id} (only when is_stock_room is "true"), {my_cost},
            {sale_rate}, {tier_quantity1}, {tier_price1}, {tier_quantity2},
            {tier_price2}, {tier_quantity3}, {tier_price3}

            Note that to set tier price options, all 6 values must be entered

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'inventories'
        return request('post', self._oauth_session, uri, body=body)
    
    def create_store_inventories(self, body: dict):
        """Creates multiple inventories in a single request. Note that you can
        create an inventory only with items in the BL Catalog.

        Arguments:
            body -- Supply a store inventory resource. The store inventory
            resource should include:
            
            {item.no}, {item.type}, {color_id}, {quantity}, {unit_price},
            {new_or_used}, {completeness} (only when item.type is "set"),
            {description}, {remarks}, {bulk}, {is_retain}, {is_stock_room},
            {stock_room_id} (only when is_stock_room is "true"), {my_cost},
            {sale_rate}, {tier_quantity1}, {tier_price1}, {tier_quantity2},
            {tier_price2}, {tier_quantity3}, {tier_price3}

            Note that to set tier price options, all 6 values must be entered

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'inventories'
        return request('post', self._oauth_session, uri, body=body)
    
    def update_store_inventory(self, inventory_id: int, body: dict):
        """Updates properties of the specified inventory.

        Arguments:
            inventory_id -- The ID of the inventory to update.

            body -- Supply a store inventory resource. The store inventory
            resource should include:
                {+quantity}, {unit_price}, {description}, {remarks}, {bulk},
                {is_retain}, {is_stock_room},
                {stock_room_id} (only when is_stock_room is "true"),
                {my_cost}, {sale_rate}, {tier_quantity1}, {tier_price1},
                {tier_quantity2}, {tier_price2}, {tier_quantity3},
                {tier_price3}

                Note that to set tier price options, all 6 values must be entered

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'inventories/{inventory_id}'
        return request('post', self._oauth_session, uri, body=body)
    
    def delete_store_inventory(self, inventory_id: int):
        """Deletes the specified inventory.

        Arguments:
            inventory_id -- The ID of the inventory to delete.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'inventories/{inventory_id}'
        return request('delete', self._oauth_session, uri)
    
class _CatalogItem(_BaseResource):
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
        uri = f'items/{type}/{no}'
        return request('get', self._oauth_session, uri)
    
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
        uri = f'items/{type}/{no}/images/{color_id}'
        return request('get', self._oauth_session, uri)
    
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
        uri = f'items/{type}/{no}/supersets'
        return request('get', self._oauth_session, uri, params)
    
    def get_subsets(self, type: str, no: str, color_id: int = None,
                      box: bool = False, instruction: bool = False,
                      break_minifigs: bool = False,
                      break_subsets: bool = False):
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
            "break_subsets": break_subsets
        }
        uri = f'items/{type}/{no}/subsets'
        return request('get', self._oauth_session, uri, params)
    
    def get_price_guide(self, type: str, no: str, color_id: int = None,
                        guide_type: str = "stock", new_or_used: str = "N",
                        country_code: str = None, region: str = None,
                        currency_code: str = None, vat: str = "N"):
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
            "vat": vat
        }
        uri = f'items/{type}/{no}/price'
        return request('get', self._oauth_session, uri, params)
    
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
        uri = f'items/{type}/{no}/colors'
        return request('get', self._oauth_session, uri)
    
class _Feedback(_BaseResource):
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
        uri = f'feedback'
        return request('get', self._oauth_session, uri, params)

    def get_feedback(self, feedback_id: int):
        """Gets a specified feedback.

        Arguments:
            feedback_id -- The ID of the feedback to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'feedback/{feedback_id}'
        return request('get', self._oauth_session, uri)
    
    def post_feedback(self, body: dict):
        """Posts a new feedback about the transaction.

        Arguments:
            body -- In the request body, supply feedback resource.
                The feedback resource object should include:
                order_id, rating and comment

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'feedback'
        return request('post', self._oauth_session, uri, body=body)
    
    def reply_feedback(self, feedback_id: int, body: dict):
        """Creates a reply to the specified feedback you received.

        Arguments:
            feedback_id -- The ID of the feedback to post a reply.

            body -- In the request body, supply feedback resource.
                The feedback resource object should include: reply

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'feedback/{feedback_id}/reply'
        return request('post', self._oauth_session, uri, body=body)

class _Color(_BaseResource):
    def get_color_list(self):
        """Retrieves a list of the colors defined within BrickLink catalog.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'colors'
        return request('get', self._oauth_session, uri)
    
    def get_color(self, color_id: int):
        """Retrieves information about a specific color.

        Arguments:
            color_id -- The ID of the color to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'colors/{color_id}'
        return request('get', self._oauth_session, uri)    

class _Category(_BaseResource):
    def get_category_list(self):
        """Retrieves a list of the categories defined within
        BrickLink catalog.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'categories'
        return request('get', self._oauth_session, uri)
    
    def get_category(self, category_id: int):
        """Retrieves information about a specific category.

        Arguments:
            category_id -- The ID of the category to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'categories/{category_id}'
        return request('get', self._oauth_session, uri)

class _PushNotification(_BaseResource):
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
        uri = f'notifications'
        return request('get', self._oauth_session, uri)

class _Coupon(_BaseResource):
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
        params = {
            "direction": direction,
            "status": status
        }
        uri = f'coupons'
        return request('get', self._oauth_session, uri, params)
    
    def get_coupon(self, coupon_id: int):
        """Retrieves a specific coupon.

        Arguments:
            coupon_id -- The ID of the coupon to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'coupons/{coupon_id}'
        return request('get', self._oauth_session, uri)
    
    def create_coupon(self, body: dict):
        """Creates a new coupon for a buyer.

        Arguments:
            body -- Supply a coupon resource.
            https://www.bricklink.com/v3/api.page?page=resource-representations-coupon    

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'coupons'
        return request('post', self._oauth_session, uri, body=body)
    
    def update_coupon(self, coupon_id: int, body: dict):
        """Updates properties of the specified coupon.

        Arguments:
            coupon_id -- The ID of the coupon to update.

            body -- Supply a coupon resource.
        https://www.bricklink.com/v3/api.page?page=resource-representations-coupon

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'coupons/{coupon_id}'
        return request('put', self._oauth_session, uri, body=body)
    
    def delete_coupon(self, coupon_id):
        """Deletes the specified coupon.

        Arguments:
            coupon_id -- The ID of the coupon to delete.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'coupons/{coupon_id}'
        return request('delete', self._oauth_session, uri)

class _Setting(_BaseResource):
    def get_shipping_methods(self):
        """Retrieves a list of shipping method you registered.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'settings/shipping_methods'
        return request('get', self._oauth_session, uri)
    
    def get_shipping_method(self, method_id: int):
        """Retrieves the specified shipping method of your store.

        Arguments:
            method_id -- The ID of the shipping method to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'settings/shipping_methods/{method_id}'
        return request('get', self._oauth_session, uri)
    
class _Member(_BaseResource):
    def get_member_rating(self, username: str):
        """Retrieves feedback ratings of a specific member.

        Arguments:
            username -- username in BrickLink.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'members/{username}/ratings'
        return request('get', self._oauth_session, uri)
    
    def get_member_note(self, username: str):
        """Retrieves your notes on a member.

        Arguments:
            username -- username in BrickLink.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'members/{username}/notes'
        return request('get', self._oauth_session, uri)
    
    def create_member_note(self, username: str, body: dict):
        """_summary_

        Arguments:
            username -- username in BrickLink.

            body -- Note resource:
        https://www.bricklink.com/v3/api.page?page=resource-representations-member

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'members/{username}/notes'
        return request('post', self._oauth_session, uri, body=body)
    
    def update_member_note(self, username: str, body: dict):
        """Updates properties of your member notes on the specified user.

        Arguments:
            username -- username in BrickLink.

            body -- Note resource:
        https://www.bricklink.com/v3/api.page?page=resource-representations-member

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'members/{username}/notes'
        return request('put', self._oauth_session, uri, body=body)
    
    def delete_member_note(self, username: str):
        """Deletes the notes on the specified user.

        Arguments:
            username -- username in BrickLink.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'members/{username}/notes'
        return request('delete', self._oauth_session, uri)
    
class _ItemMapping(_BaseResource):
    def get_element_id(self, type: str, no: str, color_id: int = None):
        """Returns Part-Color-Code (A.K.A ElementID) of the specified item.

        Arguments:
            type -- The type of an item to get. Acceptable values are: PART

            no -- Identification number of an item to get.

        Keyword Arguments:
            color_id -- Color ID of an item. If not specified, API retrieves
            element IDs of an item in any colors. (default: {None})

        Returns:
            requests.Response: The response object returned from the request.
        """
        params = {"color_id": color_id}
        uri = f'item_mapping/{type}/{no}'
        return request('get', self._oauth_session, uri, params)
    
    def get_item_number(self, element_id: str):
        """Returns BL Catalog Item Number by Part-Color-Code (A.K.A ElementID)

        Arguments:
            element_id -- Element ID of the item in specific color.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f'item_mapping/{element_id}'
        return request('get', self._oauth_session, uri)
    