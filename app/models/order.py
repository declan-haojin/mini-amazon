from flask import current_app as app


class Order:
    def __init__(self, uid, purchase_id, order_id, number_of_items, amount, status, product_id,time_purchased):
        self.uid = uid
        self.purchase_id = purchase_id
        self.order_id = order_id
        self.number_of_items = number_of_items
        self.amount= amount
        self.status = status
        self.product_id = product_id
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
        SELECT o.uid, o.purchase_id, o.order_id, o.number_of_items, o.amount, o.status, o.product_id,p.time_purchased
        FROM Orders o, Purchases p
        WHERE o.uid = :uid
        AND o.purchase_id=p.purchase_id
        ORDER BY time_purchased DESC
        ''', uid=uid)
        return [Order(*row) for row in rows]

    @staticmethod
    def create(uid, purchase_id, order_id, number_of_items, amount, product_id, status="Processing"):
        rows = app.db.execute("""
            INSERT INTO Orders(uid, purchase_id, order_id, number_of_items, amount, status, product_id)
            VALUES (:uid, :purchase_id, :order_id, :number_of_items, :amount, :status, :product_id)
            """,
            uid=uid,
            purchase_id=purchase_id,
            order_id=order_id,
            number_of_items=number_of_items,
            amount=amount,
            status=status,
            product_id=product_id)
        print(rows)
        return rows[0][0]

    @staticmethod
    def update():
        pass

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