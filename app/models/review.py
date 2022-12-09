from flask import current_app as app
from app.models.seller import Seller
from app.models.user import User
from app.models.product import Product

class Review:
    """
    A review is a way for seller to receive feedback from a user. All reviews have a unique id and map from a user to a seller.
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
        """
        get reviews based on review id
        """
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
        """
        get all reviews that are after a certain date by a specific user
        """
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
        """
        get all reviews by a specific user
        """
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
        """
        get all reviews including reviews given to a seller and to a product, 
        each review is mapped to a product even if it is a seller review since a 
        bad seller review might be for a specific seller product combination
        """
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
        """
        get all reviews specifically for products
        """
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
        """
        get all reviews that are specific to sellers 
        """
        rows = app.db.execute('''
            SELECT uid, review_id, review_content,rating, review_time, seller_id, product_id, review_type, vote
            FROM Reviews
            WHERE seller_id = :seller_id AND review_type = :review_type
            ORDER BY vote DESC
            ''',
            seller_id=seller_id, review_type="seller")
        return [Review(*row) for row in rows]

    @staticmethod
    def get_5_most_recent(uid):
        """
        get 5 most recent reviews given by the user.
        """
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
        """
        create a new product review, add information like seller, product 
        """
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
        """
        create a new seller review, add information like seller, product etc.
        """
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
        """
        get summary of product review ratings, inclduing average rating and number of ratings
        """
        avg_rating = app.db.execute('''
            SELECT AVG(rating)
            FROM Reviews
            WHERE product_id = :product_id AND review_type = :review_type
            ''',
            product_id=product_id,
            review_type="product")

        num_rating = app.db.execute('''
            SELECT COUNT(rating)
            FROM Reviews
            WHERE product_id = :product_id AND review_type = :review_type
            ''',
            product_id=product_id,
            review_type="product")

        if num_rating == [(0,)]:
            return 0, 0

        else: return '%.2f'%list(avg_rating[0])[0], list(num_rating[0])[0]

    @staticmethod
    def sum_seller_review(seller_id):
        """
        get summary of seller review ratings, inclduing average rating and number of ratings
        """
        if not seller_id:
            return 0, 0

        avg_rating = app.db.execute('''
            SELECT AVG(rating)
            FROM Reviews
            WHERE seller_id = :seller_id AND review_type = :review_type
            ''',
            seller_id=seller_id, review_type="seller")

        num_rating = app.db.execute('''
            SELECT COUNT(rating)
            FROM Reviews
            WHERE seller_id = :seller_id AND review_type = :review_type
            ''',
            seller_id=seller_id, review_type="seller")

        # print(num_rating)

        if num_rating == [(0,)]:
            return 0, 0

        else: return '%.2f'%list(avg_rating[0])[0], list(num_rating[0])[0]

# Edit/delete reviews

    @staticmethod
    def update_review(review_id, review_content, review_time, rating):
        """
        update a given review by modifying any review information
        """
        app.db.execute('''
        UPDATE Reviews
        SET review_content = :review_content, rating = :rating, review_time = :review_time
        WHERE review_id = :review_id
        ''',
        review_id=review_id, review_content=review_content, review_time=review_time, rating=rating)
        return
        
    @staticmethod
    def get_analytics_user(seller_id):
        """
        get user analytics including average rating user
        """
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
    def remove_review(review_id):
        """
        delete a review
        """
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
        """
        get seller id for a user and product combination from orders to see what product a user has ordered from which seller.
        """
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
        """
        get the products for a given user_id and seller combination based on orders
        """
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
        """
        update the vote for a given review. 
        """
        app.db.execute('''
        UPDATE Reviews
        SET vote = vote + 1
        WHERE review_id = :review_id
        ''',
        review_id=review_id)
        return
