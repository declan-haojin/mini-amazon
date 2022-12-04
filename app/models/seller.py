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
    def get_by_auth(email, password):
        rows = app.db.execute("""
            SELECT *
            FROM Sellers
            WHERE email = :email
            """,
            email=email)

        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][5], password):
            # incorrect password
            print("*******incorrect password")
            print(rows[0][5])
            print(password)

            return None
        else:
            return Seller(*(rows[0]))

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
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
            INSERT INTO Sellers(email, password, firstname, lastname)
            VALUES(:email, :password, :firstname, :lastname)
            RETURNING seller_id
            """,
            email=email,
            password=generate_password_hash(password),
            firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return Seller.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
        SELECT *
        FROM Sellers
        WHERE seller_id = :id
        """,
        id=id)
        return Seller(*(rows[0])) if rows else None
