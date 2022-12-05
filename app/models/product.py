from flask import current_app as app


class Product:
    def __init__(self, product_id, category, image, name, description, price, available, created_by):
        self.product_id = product_id
        self.category = category
        self.image = image
        self.name = name
        self.description = description
        self.price = price
        self.available = available
        self.created_by = created_by


    def __repr__(self):
        pass

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
            SELECT *
            FROM Products
            WHERE product_id = :id
            ''',
            id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT *
            FROM Products
            ORDER BY price ASC
        ''')
        return [Product(*row) for row in rows]

    @staticmethod
    def search_by_conditions(keywords, category, sort):
        if category == "All":
            if keywords == "":
                rows = app.db.execute('''
                    SELECT *
                    FROM Products
                    ORDER BY price ASC
                ''')
            else:
                rows = app.db.execute('''
                    SELECT *
                    FROM Products
                    WHERE (name iLIKE :keywords OR description iLIKE :keywords)
                    ORDER BY price ASC
                    ''',
                    keywords = '%' + keywords + '%',
                )
        else:
            if keywords == "":
                rows = app.db.execute('''
                    SELECT *
                    FROM Products
                    WHERE category = :category
                    ORDER BY price ASC
                ''',
                category = category)
            else:
                rows = app.db.execute('''
                    SELECT *
                    FROM Products
                    WHERE (name iLIKE :keywords OR description iLIKE :keywords)
                    AND category = :category
                    ORDER BY price ASC
                    ''',
                    keywords = '%' + keywords + '%',
                    category = category
                )
        if sort == 'DESC':
            return reversed([Product(*row) for row in rows])
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_categories():
        rows = app.db.execute('''
            SELECT DISTINCT(category)
            FROM Products
        ''')
        return rows

    @staticmethod
    def update(product_id, category, image, name, description, price, available):
        rows = app.db.execute("""
            UPDATE Products
            SET category=:category,
            image=:image,
            name=:name,
            description=:description,
            price=:price,
            available=:available
            WHERE product_id=:product_id
            """,
            category=category,
            image=image,
            name=name,
            description=description,
            price=price,
            available=available,
            product_id=product_id)
        print(rows)
        return None

    @staticmethod
    def create(category, image, name, description, price, available, created_by):
        rows = app.db.execute("""
            INSERT INTO Products(category, image, name, description, price, available, created_by)
            VALUES(:category, :image, :name, :description, :price, :available, :created_by)
            RETURNING product_id
            """,
            category=category,
            image=image,
            name=name,
            description=description,
            price=price,
            available=available,
            created_by=created_by)
        print(rows)
        return rows[0][0]


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

