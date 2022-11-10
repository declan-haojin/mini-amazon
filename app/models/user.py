from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, uid, firstname, lastname, address, email, password, balance):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.password = password
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
            SELECT *
            FROM Users
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
            return User(*(rows[0]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
            INSERT INTO Users(email, password, firstname, lastname)
            VALUES(:email, :password, :firstname, :lastname)
            RETURNING uid
            """,
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
        SELECT uid, email, firstname, lastname
        FROM Users
        WHERE uid = :id
        """,
                              id=id)
        return User(*(rows[0])) if rows else None
