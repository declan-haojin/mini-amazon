from flask import current_app as app


class Cart:
    def __init__(self, uid, seller_id, product_id, cart_quantity, unit_price):
        self.uid = uid
        self.seller_id = seller_id
        self.product_id = product_id
        self.cart_quantity = cart_quantity
        self.unit_price = unit_price
        self.total_price = cart_quantity*unit_price

    @staticmethod
    def get(uid, seller_id, product_id):
        rows = app.db.execute(
            '''
            SELECT *
            FROM Cart
            WHERE uid = :uid AND seller_id = :seller_id AND product_id = product_id
            ''',
            uid=uid,
            seller_id=seller_id,
            product_id=product_id)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all(uid, quantity):
        rows = app.db.execute(
        '''
        SELECT c.uid, p.name, p.product_id, cart_quantity, unit_price, (unit_price * cart_quantity) AS total_price
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

    @staticmethod
    def add_item(product_id, seller_id):
        rows = app.db.execute("""
            INSERT INTO Cart(uid, seller_id, product_id, cart_quantity, unit_price)
            VALUES(:uid, :seller_id, :product_id, :cart_quantity, :unit_price)
            RETURNING *
            """,
            category=category,
            image=image)
        print(rows)
        return rows[0][0]

# #Update quantity
#     @staticmethod
#     def update_quantity(cart_quantity, product_id):
#         app.db.execute(
#         '''
#         UPDATE Cart
#         SET cart_quantity = :cart_quantity
#         WHERE product_id = :product_id
#         ''',
#         cart_quantity=cart_quantity, product_id=product_id)
#         return
