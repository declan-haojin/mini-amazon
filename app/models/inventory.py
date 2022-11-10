from flask import current_app as app

class Inventory:
    def __init__(self, sid, pid, qty):
        self.seller_id = sid
        self.product_id = pid
        self.inventory_quantity = qty

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
        if not (sid.isdigit()):
            return "Invalid seller id, please enter an integer."
        if not (pid.isdigit()):
            return "Invalid product id, please enter an integer."
        if not (qty.isdigit()):
            return "Invalid quantity, please enter an integer."
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
            qty = int(qty)
            qty += row[0][2]
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