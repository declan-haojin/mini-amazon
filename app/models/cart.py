from flask import current_app as app


class Cart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, product_id, cart_quantity, unit_price, total_price):
        self.uid = uid
        self.product_id = product_id
        self.cart_quantity = cart_quantity
        self.unit_price = unit_price
        self.total_price = total_price


    @staticmethod
    def get(id):
        rows = app.db.execute(
        '''
        SELECT id, uid, pid, time_added_to_cart
        FROM Cart
        WHERE id = :id
        ''',
                              id=id)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute(
        '''
        SELECT id, uid, pid, time_added_to_cart
        FROM Cart
        WHERE uid = :uid
        AND time_added_to_cart >= :since
        ORDER BY time_added_to_cart DESC
        ''',
                              uid=uid,
                              since=since)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute(
        '''
        SELECT c.uid, p.name, cart_quantity, unit_price, (unit_price * cart_quantity) AS total_price
        FROM Products p, Cart c
        WHERE c.uid = :uid AND p.product_id = c.product_id
        ''',
                              uid=uid)
        return [Cart(*row) for row in rows]


    @staticmethod
    def get_all(uid, quantity):
        rows = app.db.execute(
        '''
        SELECT c.uid, p.name, cart_quantity, unit_price, (unit_price * cart_quantity) AS total_price
        FROM Products p, Cart c
        WHERE c.uid = :uid AND p.product_id = c.product_id
        ''',
                              uid=uid,
                              cart_quantity=quantity)
        return [Cart(*row) for row in rows]

#Delete item
    @staticmethod 
    def remove_item(product_id): 
        app.db.execute(
        '''
        DELETE FROM Cart
        WHERE product_id = :product_id
        ''', 
        product_id = product_id)
        return