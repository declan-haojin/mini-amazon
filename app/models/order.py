from flask import current_app as app
from app.models.purchase import Purchase
from app.models.seller import Seller
from app.models.product import Product

class Order:
    def __init__(self, uid, purchase_id, order_id, number_of_items, amount, status, product_id):
        self.uid = uid
        self.purchase_id = purchase_id
        self.order_id = order_id
        self.number_of_items = number_of_items
        self.amount= amount
        self.status = status
        self.product = Product.get(product_id)
        self.time_purchased = Purchase.get(uid).time_purchased
        self.product_name = self.product.name

        def get_seller_id():
            rows = app.db.execute("""
                SELECT seller_id
                FROM OrdersSellers os
                WHERE order_id = :order_id
                """,
                order_id=self.order_id)
            return rows[0][0] # thsi
        self.seller = Seller.get(get_seller_id())

    @staticmethod
    def get(order_id):
        rows = app.db.execute('''
            SELECT *
            FROM Orders
            WHERE order_id = :order_id
        ''', order_id=order_id)
        print(Order(*(rows[0])))
        return None
        

    # @staticmethod
    # def get(uid):
    #     rows = app.db.execute('''
    #     SELECT *
    #     FROM Orders
    #     WHERE uid = :uid
    #     ''', uid=uid)
    #     return [Order(*row) for row in rows]

    @staticmethod
    def create(uid, purchase_id, number_of_items, amount, status, product_id):
        rows = app.db.execute("""
            INSERT INTO Orders(uid, purchase_id, number_of_items, amount, status, product_id)
            VALUES (:uid, :purchase_id, :number_of_items, :amount, :status, :product_id)
            RETURNING *
            """,
            uid=uid,
            purchase_id=purchase_id,
            number_of_items=number_of_items,
            amount=amount,
            status=status,
            product_id=product_id)
        

    @staticmethod
    def update(uid, purchase_id, order_id, status):
        rows = app.db.execute("""
            UPDATE Orders
            SET status=:status
            WHERE uid=:uid AND purchase_id=:purchase_id AND order_id=:order_id
            RETURNING *
            """,
            uid=uid,
            purchase_id=purchase_id,
            order_id=order_id,
            status=status)
        return Order(*(rows[0]))



    # @staticmethod
    # def get_by_uid(uid):
    #     rows = app.db.execute("""
    #     SELECT *
    #     FROM Purchases
    #     WHERE Purchases.uid = :uid
    #     ORDER BY time_purchased DESC
    #     """
    #     ,                     uid=uid)
    #     return [Orders(*row) for row in rows]
