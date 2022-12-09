from flask import current_app as app
from datetime import datetime
from app.models.seller import Seller
from app.models.product import Product

class Order:
    """
    An order is defined is buying any quantity of a single type of product. Each order has a unique order id.
    Each purchase is constituted on multiple orders where an order is satisfied by a given specific seller, but purchase may 
    include many products by many sellers

    """
    def __init__(self, uid, purchase_id, order_id, number_of_items, amount, status, product_id, seller_id, updated_at):
        """
        initialize an order object
        """
        self.uid = uid
        self.purchase_id = purchase_id
        self.order_id = order_id
        self.number_of_items = number_of_items
        self.amount= amount
        self.status = status
        self.product_id = product_id
        self.product = Product.get(product_id)
        self.product_name = self.product.name
        self.seller_id = seller_id
        self.seller_name = Seller.get(seller_id).name
        self.updated_at = updated_at

    @staticmethod
    def get(order_id):
        """
        Get order that matches order id
        """
        rows = app.db.execute('''
            SELECT *
            FROM Orders
            WHERE order_id = :order_id
        ''', order_id=order_id)
        return Order(*(rows[0]))

    @staticmethod
    def get_by_seller_id(sid):
        """
        Get all orders by a seller ordered by time purchased in descending order
        """
        rows = app.db.execute('''
        SELECT Purchases.time_purchased, Orders.product_id, Orders.number_of_items, Orders.uid, Orders.order_id, Users.address, Orders.status
        FROM Orders, Purchases, Users
        WHERE Orders.seller_id = :sid
        AND Purchases.purchase_id = Orders.purchase_id
        AND Orders.uid = Users.uid
        ORDER BY Purchases.time_purchased DESC
        ''',
        sid=sid)
        return rows


    @staticmethod
    def create(uid, purchase_id, number_of_items, amount, status, product_id, seller_id):
        """
        Create a new order and add amount, status, product_id etc.
        """
        rows = app.db.execute("""
            INSERT INTO Orders(uid, purchase_id, number_of_items, amount, status, product_id, seller_id, updated_at)
            VALUES (:uid, :purchase_id, :number_of_items, :amount, :status, :product_id, :seller_id, :updated_at)
            RETURNING *
            """,
            uid=uid,
            purchase_id=purchase_id,
            number_of_items=number_of_items,
            amount=amount,
            status=status,
            product_id=product_id,
            seller_id=seller_id,
            updated_at=datetime.now())
        return Order(*(rows[0]))

    def update(self, status):
        """
        Update an order status based on seller fulfillment 
        """
        rows = app.db.execute("""
            UPDATE Orders
            SET status=:status
            WHERE order_id=:order_id
            RETURNING *
            """,
            order_id=self.order_id,
            status=status)
        return Order(*(rows[0]))

    @staticmethod
    def get_by_purchase_id(purchase_id):
        """
        Get orders by purchase id. Each purchase can have multiple orders. 
        """
        rows = app.db.execute('''
            SELECT *
            FROM Orders
            WHERE purchase_id = :purchase_id
        ''', purchase_id=purchase_id)
        return [Order(*row) for row in rows]