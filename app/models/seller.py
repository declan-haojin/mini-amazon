from flask import current_app as app
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

class Seller():
    """
    A seller is a person who can sell products, create products, hold inventory and fulfil orders.
    """
    def __init__(self, sid, balance, firstname, lastname, address, email, password):
        """
        create seller
        """
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
        """
        get all seller information by seller id 
        """
        rows = app.db.execute('''
        SELECT *
        FROM Sellers
        WHERE seller_id = :sid
        ''',
        sid=sid)
        return Seller(*(rows[0])) if rows else None

    @staticmethod
    def get_by_sid(sid):
        """
        get seller name by seller id
        """
        rows = app.db.execute('''
        SELECT firstname, lastname
        FROM Sellers
        WHERE seller_id = :sid
        ''',
        sid=sid)
        return [record._mapping for record in rows][0]


    @staticmethod
    def create(fname, lname, email, pwd):
        """
        create a new seller using firstname lastname and password
        """

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
        """
        check if email exists in database
        """
        rows = app.db.execute("""
        SELECT email
        FROM Sellers
        WHERE email = :email
        """,
                              email=email)
        return len(rows) > 0

    @staticmethod
    def update(seller_id, firstname, lastname, address, email, password,):
        """
        update seller information.
        """
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
        """
        allow seller to withdraw balance
        """
        rows = app.db.execute("""
        UPDATE Sellers 
        SET balance=0
        WHERE seller_id = :seller_id
        """,seller_id = seller_id)
        return None

    @staticmethod
    def topup_balance(seller_id,payment):
        """
        allow seller to add abalance
        """
        app.db.execute("""
        UPDATE Sellers 
        SET balance=balance+:payment
        WHERE seller_id = :seller_id
        """,seller_id = seller_id, payment = payment)
        return None
    
    @staticmethod
    def public_profile(seller_id):
        """
        see seller public profile
        """
        rows=app.db.execute("""
        SELECT * 
        FROM Sellers
        WHERE seller_id=:seller_id
        """,seller_id=seller_id)
        return [Seller(*row) for row in rows]

    