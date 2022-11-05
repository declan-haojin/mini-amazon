from flask import current_app as app


class Purchase:
    def __init__(self, uid,  num_order, total_amount, time_purchased):
        self.uid = uid
        # self.pid = pid
        self.num_order=num_order
        self.total_amount=total_amount
        # self.status=status
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
        SELECT uid, pid, num_order, total_amount, status, time_purchased
        FROM Purchases
        WHERE uid = :uid
        ''', uid=uid)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute("""
        SELECT uid,num_order, total_amount,time_purchased
        FROM Purchases
        WHERE Purchases.uid = :uid
        ORDER BY time_purchased DESC
        """
        ,                     uid=uid)
        return [Purchase(*row) for row in rows]

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
