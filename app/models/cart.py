from flask import current_app as app
from app.models.seller import Seller
from app.models.product import Product


class Cart:
    def __init__(self, uid, seller_id, product_id, cart_quantity):
        self.uid = uid
        self.seller_id = seller_id
        self.product_id = product_id
        self.cart_quantity = cart_quantity
        self.seller_name = Seller.get_by_sid(seller_id).firstname + " " + Seller.get_by_sid(seller_id).lastname
        self.product_name = Product.get(product_id).name
        self.unit_price = Product.get(product_id).price
        self.total_price = self.unit_price * cart_quantity


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

    def update(uid, seller_id, product_id, cart_quantity):
        rows = app.db.execute("""
            UPDATE Cart
            SET cart_quantity=:cart_quantity
            WHERE uid=:uid AND seller_id=:seller_id AND product_id=:product_id
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
    def delete(uid, seller_id, product_id):
        app.db.execute(
        '''
        DELETE FROM Cart
        WHERE uid = :uid AND seller_id = :seller_id AND product_id = product_id
            ''',
            uid=uid,
            seller_id=seller_id,
            product_id=product_id)
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