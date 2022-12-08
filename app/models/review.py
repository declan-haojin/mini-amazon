from flask import current_app as app
from app.models.seller import Seller
from app.models.user import User
from app.models.product import Product

class Review:
    """
    This is just a TEMPLATE for Review, you should change this by adding or
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, id, review_content,rating, review_time, sid, pid, review_type, vote=0):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review_time = review_time
        self.review_content = review_content
        self.sid = sid
        self.rating = rating
        self.review_type = review_type
        self.user_name = User.get(uid).name
        self.seller_name = Seller.get(sid).name
        self.vote = vote
        self.product_name = Product.get(pid).name

# get reviews

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
    def get_all_product_review_by_pid(product_id):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type
            FROM Reviews
            WHERE product_id = :product_id AND review_type = :review_type
            ORDER BY review_time DESC
            ''',
            product_id=product_id,
            review_type="product")
        return [Review(*row) for row in rows]

    @staticmethod
    def get_all_by_sid(seller_id):
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type, vote
            FROM Reviews
            WHERE seller_id = :seller_id
            ORDER BY vote DESC
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


# add reviews

    @staticmethod
    def create_product_review(uid, content, rating, time, seller_id, product_id, review_type="product", vote=0):
        check = app.db.execute("""
        SELECT review_id
        FROM Reviews
        WHERE uid = :uid AND seller_id = :seller_id AND product_id = :product_id AND review_type = :review_type
        """
        ,uid=uid, seller_id=seller_id, product_id = product_id, review_type = review_type)

        if not check:
            app.db.execute('''
                        INSERT INTO Reviews(uid, review_content, rating, review_time, seller_id, product_id, review_type, vote)
                        VALUES(:uid, :content, :rating, :time, :seller_id, :product_id, :review_type, :vote)
                ''',
                uid=uid, content=content, rating=rating, time=time, seller_id=seller_id, product_id=product_id, review_type=review_type, vote=vote)
            return False
        else: return True


    @staticmethod
    def create_seller_review(uid, content, rating, time, seller_id, product_id, review_type="seller", vote=0):
        check = app.db.execute("""
        SELECT review_id
        FROM Reviews
        WHERE uid = :uid AND seller_id = :seller_id AND product_id = :product_id AND review_type = :review_type
        """
        ,uid=uid, seller_id=seller_id, product_id = product_id, review_type = review_type)

        if not check:
            app.db.execute('''
                INSERT INTO Reviews(uid, review_content, rating, review_time, seller_id, product_id, review_type, vote)
                VALUES(:uid, :content, :rating, :time, :seller_id, :product_id, :review_type, :vote)
                ''',
                uid=uid, content=content, rating=rating, time=time, seller_id=seller_id, product_id=product_id, review_type=review_type, vote=vote)
            return False

        else: return True

    @staticmethod
    def sum_product_review(product_id):
        avg_rating = app.db.execute('''
            SELECT AVG(rating)
            FROM Reviews
            WHERE product_id = :product_id
            ''',
            product_id=product_id)

        num_rating = app.db.execute('''
            SELECT COUNT(rating)
            FROM Reviews
            WHERE product_id = :product_id
            ''',
            product_id=product_id)

        if num_rating == [(0,)]:
            return 0, 0

        else: return '%.2f'%list(avg_rating[0])[0], list(num_rating[0])[0]

    @staticmethod
    def sum_seller_review(seller_id):
        if not seller_id:
            return 0, 0

        avg_rating = app.db.execute('''
            SELECT AVG(rating)
            FROM Reviews
            WHERE seller_id = :seller_id
            ''',
            seller_id=seller_id)

        num_rating = app.db.execute('''
            SELECT COUNT(rating)
            FROM Reviews
            WHERE seller_id = :seller_id
            ''',
            seller_id=seller_id)

        # print(num_rating)

        if num_rating == [(0,)]:
            return 0, 0

        else: return '%.2f'%list(avg_rating[0])[0], list(num_rating[0])[0]

# Edit/delete reviews

    @staticmethod
    def update_review(review_id, review_content, review_time, rating):
        app.db.execute('''
        UPDATE Reviews
        SET review_content = :review_content, rating = :rating, review_time = :review_time
        WHERE review_id = :review_id
        ''',
        review_id=review_id, review_content=review_content, review_time=review_time, rating=rating)
        return


    @staticmethod
    def remove_review(review_id):
        if type(review_id) == int or review_id.isdigit():
            app.db.execute('''
            DELETE FROM Reviews
            WHERE review_id = :review_id
            ''',
            review_id = review_id)
        return

# Get seller_id or product_id

    @staticmethod
    def get_seller_id(uid, product_id):
        row = app.db.execute('''
        SELECT seller_id
        FROM Orders
        Where uid = :uid AND product_id = :product_id
        ''',
        uid=uid, product_id=product_id)

        if not row:
            return None

        else: return list(row[0])[0]

    @staticmethod
    def get_product_id(uid, seller_id):
        row = app.db.execute('''
        SELECT product_id
        FROM Orders
        WHERE uid = :uid AND seller_id = :seller_id
        ''',
        uid=uid, seller_id=seller_id)

        if not row :
            return None

        else: return list(row[0])[0]


# update vote
    @staticmethod
    def update_vote(review_id):
        app.db.execute('''
        UPDATE Reviews
        SET vote = vote + 1
        WHERE review_id = :review_id
        ''',
        review_id=review_id)
        return
