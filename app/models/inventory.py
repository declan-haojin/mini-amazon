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
        print(rows)
        return rows

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
        print(rows)
        return rows

    @staticmethod
    def add_item_to_inventory(sid, pid, qty):
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
            return ["Added new item", sid, pid, qty]
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
            return ["Modified count", sid, pid, qty]