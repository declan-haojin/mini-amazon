from flask import current_app as app
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

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

    @staticmethod
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

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
        SELECT email
        FROM Sellers
        WHERE email = :email
        """,
                              email=email)
        return len(rows) > 0

    @staticmethod
    def update(seller_id, firstname, lastname, address, email, password,):
        app.db.execute("""
        UPDATE Sellers 
        SET email=:email, password=:password,firstname=:firstname,lastname=:lastname, address=:address
        WHERE seller_id = :seller_id
        """,
        seller_id=seller_id, email=email, password=generate_password_hash(password), firstname=firstname,lastname=lastname, address=address)
        app.db.execute("""
        UPDATE Users 
        SET email=:email, password=:password
        WHERE uid = :seller_id
        """,
        seller_id=seller_id, email=email, password=generate_password_hash(password))
        return None

    @staticmethod
    def withdraw_balance(seller_id):
        rows = app.db.execute("""
        UPDATE Sellers 
        SET balance=0
        WHERE seller_id = :seller_id
        """,seller_id = seller_id)
        return None

    @staticmethod
    def topup_balance(seller_id,payment):
        rows = app.db.execute("""
        UPDATE Sellers 
        SET balance=balance+:payment
        WHERE seller_id = :seller_id
        """,seller_id = seller_id, payment = payment)
        return None