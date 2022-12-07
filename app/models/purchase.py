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
        self.status = self.check_status()

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
        orders = Order.get_by_purchase_id(self.purchase_id)

        # Check if all orders of the purchase is fulfilled, the status of the purchase should also be fulfilled
        all_fulfilled = True
        for order in orders:
            if order.status != "Fulfilled":
                all_fulfilled = False
                break
        if all_fulfilled:
            self.status = "Fulfilled"
            self.update(status="Fulfilled")
        return orders

    def check_status(self):
        if self.status == "Fulfilled":
            return "Fulfilled"
        orders = Order.get_by_purchase_id(self.purchase_id)
        # Check if all orders of the purchase is fulfilled, the status of the purchase should also be fulfilled
        all_fulfilled = True
        for order in orders:
            if order.status != "Fulfilled":
                all_fulfilled = False
                break
        if all_fulfilled:
            self.status = "Fulfilled"
            self.update(status="Fulfilled")
        return self.status

    @staticmethod
    def search_by_conditions(uid,start, end, status,minamt,maxamt,seller_id):

        #status and seller ID specified
        # only seller ID
        # only status
        # neither

        if (seller_id==""):
            if (status=="All"):
                rows = app.db.execute('''
                    SELECT *
                    FROM Purchases
                    WHERE uid = :uid
                    AND time_purchased BETWEEN CAST (:start AS DATE) AND CAST (:end AS DATE)
                    AND total_amount BETWEEN CAST (:minamt AS INTEGER) AND CAST (:maxamt AS INTEGER)
                    ORDER BY time_purchased DESC;
                ''', uid=uid, start=start,end=end, minamt=minamt,maxamt=maxamt)
                return [Purchase(*row) for row in rows]
            else:
                rows = app.db.execute('''
                    SELECT *
                    FROM Purchases
                    WHERE uid = :uid
                    AND time_purchased BETWEEN CAST (:start AS DATE) AND CAST (:end AS DATE)
                    AND total_amount BETWEEN CAST (:minamt AS INTEGER) AND CAST (:maxamt AS INTEGER)
                    AND status = CAST (:status AS VARCHAR)
                    ORDER BY time_purchased DESC;
                ''', uid=uid, start=start,end=end,minamt=minamt,maxamt=maxamt,status=status)
                return [Purchase(*row) for row in rows]
        else:
            if (status=="All"):
                rows = app.db.execute('''
                        SELECT Purchases.uid,Purchases.purchase_id,Purchases.number_of_orders,Purchases.total_amount,Purchases.status,Purchases.time_purchased
                        FROM Orders, Purchases
                        WHERE Orders.purchase_id=Purchases.purchase_id
                        AND Orders.uid = Purchases.uid
                        AND Orders.uid = :uid
                        AND Purchases.time_purchased BETWEEN CAST (:start AS DATE) AND CAST (:end AS DATE)
                        AND Purchases.total_amount BETWEEN CAST (:minamt AS INTEGER) AND CAST (:maxamt AS INTEGER)
                        AND Orders.seller_id=:seller_id
                        ORDER BY time_purchased DESC;
                    ''', uid=uid, start=start,end=end,minamt=minamt,maxamt=maxamt,seller_id=seller_id)
                return [Purchase(*row) for row in rows]
            else :
                rows = app.db.execute('''
                        SELECT Purchases.uid,Purchases.purchase_id,Purchases.number_of_orders,Purchases.total_amount,Purchases.status,Purchases.time_purchased
                        FROM Orders, Purchases
                        WHERE Orders.purchase_id=Purchases.purchase_id
                        AND Orders.uid = Purchases.uid
                        AND Orders.uid = :uid
                        AND Purchases.time_purchased BETWEEN CAST (:start AS DATE) AND CAST (:end AS DATE)
                        AND Purchases.total_amount BETWEEN CAST (:minamt AS INTEGER) AND CAST (:maxamt AS INTEGER)
                        AND Purchases.status=:status
                        AND Orders.seller_id=:seller_id
                        ORDER BY time_purchased DESC;
                    ''', uid=uid, start=start,end=end,minamt=minamt,maxamt=maxamt,seller_id=seller_id,status=status)
                return [Purchase(*row) for row in rows]

    def update(self, status):
        rows = app.db.execute("""
            UPDATE Purchases
            SET status=:status
            WHERE purchase_id=:purchase_id
            RETURNING *
            """,
            status=status,
            purchase_id=self.purchase_id)
        return True

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

