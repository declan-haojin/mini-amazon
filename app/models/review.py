from flask import current_app as app


class Review:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, id, uid, pid, sid, review_time, review_content, rating):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review_time = review_time
        self.review_content = review_content
        self.sid = sid
        self.rating = rating

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, review_time, review_content, sid, rating 
FROM Reviews
WHERE id = :id
''',
                              id=id)
        return Review(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, rating, review_time, review_content
FROM Reviews
WHERE uid = :uid
AND review_time >= :since
ORDER BY review_time DESC
''',
                              uid=uid,
                              since=since)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_k_most_recent(k, uid):
        rows = app.db.execute('''
            SELECT uid, review_content
            FROM Reviews
            WHERE uid = :uid
            ORDER BY review_time DESC
            LIMIT :k
            ''',
            k=k)
        return [Review(*row) for row in rows]
