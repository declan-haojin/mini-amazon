from flask import current_app as app
from app.models.purchase import Purchase
from app.models.seller import Seller
from app.models.product import Product
class Inventory:
    def __init__(self, sid, pid, qty):
        self.seller_id = sid
        self.product_id = pid
        self.inventory_quantity = qty
        self.product = Product.get(pid)


    @staticmethod
    def get(seller_id, product_id):
        rows = app.db.execute('''
        SELECT *
        FROM Inventories
        WHERE seller_id = :seller_id AND product_id = :product_id
        ''',
        seller_id=seller_id,
        product_id=product_id)
        return Inventory(*(rows[0])) if rows else None


    @staticmethod
    def delete(product_id):
        app.db.execute('''
        DELETE FROM Inventories
        WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return


    @staticmethod
    def update(sid, pid, qty):
        rows = app.db.execute('''
            UPDATE Inventories
            SET inventory_quantity = :qty
            WHERE seller_id = :sid AND product_id = :pid
            RETURNING *
            ''',
            sid = sid,
            pid = pid,
            qty = qty
        )
        return Inventory(*(rows[0])) if rows else None


    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
        SELECT Products.product_id, Products.name, Inventories.inventory_quantity
        FROM Inventories, Products
        WHERE Inventories.seller_id = :sid
        AND Inventories.product_id = Products.product_id
        ORDER BY Products.product_id
        ''',
        sid=sid)
        return rows


    @staticmethod
    def add_item_to_inventory(sid, pid, qty):
        if not (pid.isdigit()):
            return "Invalid product id, please enter an integer."
        if not (qty.isdigit()):
            return "Invalid quantity, please enter an integer."
        if (int(sid) > 2147483647) :
            return "seller id out of range."
        if (int(pid) > 2147483647) :
            return "product id out of range."
        i = app.db.execute('''
        SELECT COUNT(*)
        FROM Products
        WHERE product_id = :pid
        ''',
        pid = pid
        )
        if (i[0][0]==0):
            return "No such product, please create the new product."
        row = app.db.execute('''
        SELECT Inventories.seller_id, Inventories.product_id, Inventories.inventory_quantity
        FROM Inventories
        WHERE Inventories.seller_id = :sid
        AND Inventories.product_id = :pid
        ''',
        sid = sid,
        pid = pid
        )

        if row == []:
            qty = int(qty)
            app.db.execute('''
            INSERT INTO Inventories VALUES (:sid, :pid, :qty)
            ''',
            sid = sid,
            pid = pid,
            qty = qty
            )
            retstr = "Seller " + str(sid) + ": You have successfully added " + str(qty) + " units of item " + str(pid) + " to your inventory."
            return retstr
        else:
            app.db.execute('''
            UPDATE Inventories
            SET inventory_quantity = :qty
            WHERE seller_id = :sid AND product_id = :pid
            ''',
            sid = sid,
            pid = pid,
            qty = qty
            )
            retstr = "Seller " + str(sid) + ": You have successfully modified the count of item " + str(pid) + " to " + str(qty) + "."
            return retstr


    @staticmethod
    def get_order(sid):
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
    def get_by_pid(pid):
        rows = app.db.execute('''
        SELECT seller_id, inventory_quantity
        FROM Inventories
        WHERE Inventories.product_id = :pid
        ''',
        pid=pid)
        query_dict = [record._mapping for record in rows]
        return query_dict


    @staticmethod
    def get_status(order_id):
        str = app.db.execute('''
        SELECT status
        FROM Orders
        WHERE order_id = :order_id
        ''',
        order_id=order_id)
        return str


    @staticmethod
    def change_order_status_spc(order_id, status):
        app.db.execute('''
        UPDATE Orders
        SET status = :status
        WHERE order_id = :order_id
        ''',
        status=status,
        order_id=order_id)
        return


    @staticmethod
    def get_analytics_category(seller_id):
        rows = app.db.execute('''
        SELECT Products.category, COUNT(*), SUM(Inventories.inventory_quantity)
        FROM Inventories, Products
        WHERE Inventories.seller_id = :seller_id
        AND Inventories.product_id = Products.product_id
        GROUP BY Products.category
        ''',
        seller_id=seller_id)
        return rows


    @staticmethod
    def get_analytics_order(seller_id, start, end):
        rows = app.db.execute('''
        SELECT Orders.product_id, Products.name, SUM(Orders.number_of_items)
        FROM Orders, Products, Purchases
        WHERE Orders.seller_id = :seller_id
        AND Orders.product_id = Products.product_id
        AND Purchases.purchase_id = Orders.purchase_id
        AND Purchases.time_purchased BETWEEN CAST (:start AS DATE) AND CAST (:end AS DATE)
        GROUP BY Orders.product_id, Products.name
        ORDER BY SUM(Orders.number_of_items) DESC
        ''',
        seller_id = seller_id,
        start = start,
        end = end)
        return rows

    
    @staticmethod
    def get_analytics_user(seller_id):
        rows = app.db.execute('''
        SELECT uid, COUNT(*), CAST(AVG(Reviews.rating) as DECIMAL(10,2))
        FROM Reviews
        WHERE Reviews.seller_id = :seller_id
        GROUP BY uid
        ORDER BY COUNT(*) DESC
        ''',
        seller_id = seller_id,)
        return rows

    @staticmethod
    def recommend(uid):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE Products.category IN (
            SELECT Products.category
            FROM Orders, Products
            WHERE uid = :uid
            AND Orders.product_id = Products.product_id
            GROUP BY Products.category
            ORDER BY COUNT(*) DESC
            LIMIT 3)
        AND Products.product_id IN (
            SELECT product_id
            FROM Orders
            GROUP BY product_id
            ORDER BY COUNT(*) DESC
            LIMIT 50
        )
        LIMIT 5
        ''',
        uid = uid)
        return [Product(*row) for row in rows]