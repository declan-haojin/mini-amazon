from flask import current_app as app


class Product:
    def __init__(self, product_id, category, image, name, description, price, available):
        self.product_id = product_id
        self.category = category
        self.image = image
        self.name = name
        self.description = description
        self.price = price
        self.available = available


    def __repr__(self):
        pass

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
            SELECT product_id, category, image, name, description, price, available
            FROM Products
            WHERE product_id = :id
            ''',
            id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
            SELECT *
            FROM Products
        ''')
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_keywords(keywords):
        rows = app.db.execute('''
            SELECT *
            FROM Products
            WHERE name iLIKE :keywords
            OR description iLIKE :keywords
            ''',
        keywords = '%' + keywords + '%')
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_categories():
        rows = app.db.execute('''
            SELECT DISTINCT(category)
            FROM Products
        ''')
        return rows





    @staticmethod
    def get_k_most_expensive(k):
        rows = app.db.execute('''
            SELECT product_id, name, price, available
            FROM Products
            ORDER BY price DESC
            LIMIT :k
            ''',
            k=k)
        return [Product(*row) for row in rows]
