from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Seller(UserMixin):
    def __init__(self, sid, balance, firstname, lastname, address, email, password):
        self.sid = sid
        self.id = sid
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.password = password
        self.balance = 0 if balance == None else balance

    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
        SELECT firstname, lastname
        FROM Sellers
        WHERE seller_id = :sid
        ''',
        sid=sid)
        return [record._mapping for record in rows][0]

    @staticmethod
    def get_seller_object(sid):
        rows = app.db.execute("""
        SELECT *
        FROM Sellers
        WHERE seller_id = :sid
        """,
        sid=sid)
        return Seller(*(rows[0])) if rows else None
