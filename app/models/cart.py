from flask import current_app as app


class Cart:
    def __init__(self, uid, seller_id, product_id, cart_quantity):
        self.uid = uid
        self.seller_id = seller_id
        self.product_id = product_id
        self.cart_quantity = cart_quantity

    @staticmethod
    def create(uid, seller_id, product_id, cart_quantity):
        rows = app.db.execute("""
            INSERT INTO Cart(uid, seller_id, product_id, cart_quantity)
            VALUES(:uid, :seller_id, :product_id, :cart_quantity)
            RETURNING *
            """,
            uid=uid,
            seller_id=seller_id,
            product_id=product_id,
            cart_quantity=cart_quantity)
        return Cart(*(rows[0]))

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
    def get_all(uid):
        rows = app.db.execute(
            '''
                SELECT *
                FROM Cart
                WHERE uid = :uid
            ''',
            uid=uid)
        return [Cart(*row) for row in rows]



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
