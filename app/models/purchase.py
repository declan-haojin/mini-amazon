from datetime import datetime
from flask import current_app as app
from app.models.order import Order



class Purchase:
    """
    A purchase is defined as one checkout of the cart, which may include multiple orders being checked out. 
    An purchase has a unique id and we record the time of purchase.
    """
    def __init__(self, uid, purchase_id, number_of_orders, total_amount, status, time_purchased):
        """
        initialize a purchase object. 
        """
        self.uid = uid
        self.purchase_id = purchase_id
        self.number_of_orders = number_of_orders
        self.total_amount= total_amount
        self.status = status
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid):
        """
        get all purchases for a given user;
        FUNCTION OBSOLETE (USED IN HW4), USE get_by_uid(uid)
        """
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE uid = :uid
        ''', uid=uid)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_by_purchase_id(purchase_id):
        """
        get purchase by purchase id
        """
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE purchase_id = :purchase_id
        ''', purchase_id=purchase_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_by_uid(uid):
        """
        get all purchases by user id 
        """
        rows = app.db.execute("""
        SELECT *
        FROM Purchases
        WHERE Purchases.uid = :uid
        ORDER BY time_purchased DESC
        """
        ,                     uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def create_purchase(uid,number_of_orders, total_amount, status):
        """
        create a new purchase 
        """
        rows = app.db.execute('''
        INSERT INTO Purchases(uid,  number_of_orders, total_amount, status, time_purchased)
        VALUES(:uid, :number_of_orders, :total_amount, :status, :time_purchased)
        RETURNING *
        ''',uid=uid, number_of_orders=number_of_orders, total_amount=total_amount, status=status, time_purchased=datetime.now())
        return Purchase(*(rows[0])) if rows else None

    def get_orders(self):
        """
        Check if all orders of the purchase is fulfilled, the status of the purchase should also be fulfilled
        """
        orders = Order.get_by_purchase_id(self.purchase_id)
        self.update_status()
        return orders

    def update_status(self):
        """
        update purchase status based on constitutent order status, if all constituent orders are fulfilled then this should be fulfilled.
        """
        orders = Order.get_by_purchase_id(self.purchase_id)
        all_fulfilled = True
        for order in orders:
            if order.status != "Fulfilled":
                all_fulfilled = False
                break
        if all_fulfilled:
            self.status = "Fulfilled"
            self.update(status="Fulfilled")
        return self.status
    
    def update(self, status):
        """
        update purchase status to reflect fulfillment conditions. Allows to update entire purchase status
        """
        rows = app.db.execute("""
            UPDATE Purchases
            SET status=:status
            WHERE purchase_id=:purchase_id
            RETURNING *
            """,
            status=status,
            purchase_id=self.purchase_id)
        return True

    @staticmethod
    def search_by_conditions(uid,start, end, status,minamt,maxamt,seller_id):
        """
        Filter purchases to find relevant purchases, filter by amount range, date range and status.
        
        """

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

