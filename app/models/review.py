from flask import current_app as app


class Review:
    """
    This is just a TEMPLATE for Review, you should change this by adding or
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, id, review_content,rating, review_time, sid, pid, review_type):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review_time = review_time
        self.review_content = review_content
        self.sid = sid
        self.rating = rating
        self.review_type = review_type

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, uid, pid, review_time, review_content, sid, rating 
            FROM Reviews
            WHERE id = :id
            ORDER BY review_time DESC
            ''',
            id=id)
        return Review(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type
            FROM Reviews
            WHERE uid = :uid
            AND review_time >= :since
            ORDER BY review_time DESC
            ''',
            uid=uid,
            since=since)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type
            FROM Reviews
            WHERE uid = :uid
            ORDER BY review_time DESC
            ''',
            uid=uid)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_all_by_pid(product_id):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type
            FROM Reviews
            WHERE product_id = :product_id
            ORDER BY review_time DESC
            ''',
            product_id=product_id)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_all_by_sid(seller_id):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type
            FROM Reviews
            WHERE seller_id = :seller_id
            ORDER BY review_time DESC
            ''',
            seller_id=seller_id)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_5_most_recent(uid):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type
            FROM Reviews
            WHERE uid = :uid
            ORDER BY review_time DESC
            LIMIT 5
            ''',
            uid=uid)
        return [Review(*row) for row in rows]


    @staticmethod
    def create_product_review(uid, content, rating, time, seller_id, product_id, review_type="product"):
        app.db.execute('''
            INSERT INTO Reviews(uid, review_content, rating, review_time, seller_id, product_id, review_type)
            VALUES(:uid, :content, :rating, :time, :seller_id, :product_id, :review_type)
            ''',
            uid=uid, content=content, rating=rating, time=time, seller_id=seller_id, product_id=product_id, review_type=review_type)
        return 
        

    @staticmethod
    def create_seller_review(uid, content, rating, time, seller_id, product_id, review_type="seller"):
        app.db.execute('''
            INSERT INTO Reviews(uid, review_content, rating, review_time, seller_id, product_id, review_type)
            VALUES(:uid, :content, :rating, :time, :seller_id, :product_id, :review_type)
            ''',
            uid=uid, content=content, rating=rating, time=time, seller_id=seller_id, product_id=product_id, review_type=review_type)
        return 
