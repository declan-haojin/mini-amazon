from datetime import datetime
from flask import current_app as app
from app.models.order import Order



class Purchase:
    def __init__(self, uid, purchase_id, number_of_orders, total_amount, status, time_purchased):
        self.uid = uid
        self.purchase_id = purchase_id
        self.number_of_orders = number_of_orders
        self.total_amount= total_amount
        self.status = status
        self.time_purchased = time_purchased
        
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE uid = :uid
        ''', uid=uid)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_by_purchase_id(purchase_id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE purchase_id = :purchase_id
        ''', purchase_id=purchase_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute("""
        SELECT *
        FROM Purchases
        WHERE Purchases.uid = :uid
        ORDER BY time_purchased DESC
        """
        ,                     uid=uid)
        return [Purchase(*row) for row in rows]

    # TODO: Purchase create method
    @staticmethod
    def create_purchase(uid,number_of_orders, total_amount, status):
        rows = app.db.execute('''
        INSERT INTO Purchases(uid,  number_of_orders, total_amount, status, time_purchased)
        VALUES(:uid, :number_of_orders, :total_amount, :status, :time_purchased)
        RETURNING *
        ''',uid=uid, number_of_orders=number_of_orders, total_amount=total_amount, status=status, time_purchased=datetime.now())
        return Purchase(*(rows[0])) if rows else None

    def get_orders(self):
        return Order.get_by_purchase_id(self.purchase_id)
    
    @staticmethod
    def search_by_conditions(uid,start, end, keywords):
        rows = app.db.execute('''
            SELECT *
            FROM Purchases
            WHERE uid = :uid
            AND time_purchased BETWEEN CAST (:start AS DATE) AND CAST (:end AS DATE)
            ORDER BY time_purchased DESC;
        ''', uid=uid, start=start,end=end)
        return [Purchase(*row) for row in rows]

    # def add_order(self, order_id):
    #     rows = app.db.execute('''
    #     INSERT INTO PurchasesOrders(purchase_id, order_id)
    #     VALUES(:purchase_id, :order_id)
    #     ''',
    #     purchase_id=self.purchase_id,
    #     order_id=order_id)

    #     return True

    # @staticmethod
    # def get_all_by_uid_since(uid, since):
        # rows = app.db.execute('''
        # SELECT id, uid, pid, time_purchased
        # FROM Purchases
        # WHERE uid = :uid
        # AND time_purchased >= :since
        # ORDER BY time_purchased DESC
        # ''',
        #                       uid=uid,
        #                       since=since)
        # return [Purchase(*row) for row in rows]

