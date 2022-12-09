from flask import current_app as app
from app.models.product import Product
class Inventory:
    """
    An inventory is defined as the number of products of each type that a seller holds. It holds information on Product ID, Seller ID and quantity and 
    """
    def __init__(self, sid, pid, qty):
        """
        initialize an inventory object.
        """
        self.seller_id = sid
        self.product_id = pid
        self.inventory_quantity = qty
        self.product = Product.get(pid)


    @staticmethod
    def get(seller_id, product_id):
        """
        Retrieve inventory for a specific seller for a given product. 
        """
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
        """
        Allows to delete inventory for a specific product(if a product is to be removed from directory for malfunction.)
        """
        app.db.execute('''
        DELETE FROM Inventories
        WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return


    @staticmethod
    def update(sid, pid, qty):
        """
        Update seller(sid) inventory for a specific product(pid) by specifying quantity
        """
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
        """
        Retrieve entire inventory for the seller for all products. Used in seller information tables. 
        """
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
        """
        Allows to add a single product to inventory provided product exists in Products
        (otherwise new product must first be created). Seller can specify product(pid) and the quantity(qty) to add.
        """
        # check for valud pid
        if not (pid.isdigit()):
            return "Invalid product id, please enter an integer."
        # check for valud qty
        if not (qty.isdigit()):
            return "Invalid quantity, please enter an integer."
        if (int(sid) > 2147483647) :
            return "seller id out of range."
        if (int(pid) > 2147483647) :
            return "product id out of range."
        #get count of products that match product id
        i = app.db.execute('''
        SELECT COUNT(*)
        FROM Products
        WHERE product_id = :pid
        ''',
        pid = pid
        )
        #return if no product with the correct ID exists
        if (i[0][0]==0):
            return "No such product, please create the new product."
        # check matching inventories for seller, for given product
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
            # add to inventory a new 
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
            # add to inventory
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
    def get_by_pid(pid):
        """
        Get inventory for pid
        """
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
        """
        Get order status
        """
        str = app.db.execute('''
        SELECT status
        FROM Orders
        WHERE order_id = :order_id
        ''',
        order_id=order_id)
        return str


    @staticmethod
    def change_order_status_spc(order_id, status):
        """
        change order status
        """
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
        """
        Get analytics on category of sales, including count of products sold by category for a given seller.
        """
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
        """
        Get analytics on category on orders, including count of products sold by category for a given seller.
        """
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

    
    

    