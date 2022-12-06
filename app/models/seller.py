from flask import current_app as app
from flask import url_for

class Seller():
    def __init__(self, sid, balance, firstname, lastname, address, email, password):
        self.sid = sid
        self.id = sid
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.password = password
        self.balance = 0 if balance == None else balance
        self.name = firstname + " " + lastname
        self.link = url_for('seller.index', sid=sid)

    @staticmethod
    def get(sid):
        rows = app.db.execute('''
        SELECT *
        FROM Sellers
        WHERE seller_id = :sid
        ''',
        sid=sid)
        return Seller(*(rows[0])) if rows else None

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

    def create(fname, lname, email, pwd):
        app.db.execute("""
        INSERT INTO Sellers(balance, firstname, lastname, email, password)
        VALUES(:balance, :firstname, :lastname, :email, :password)
        """,
        balance = 0,
        firstname = fname,
        lastname = lname,
        email = email,
        password = pwd)
