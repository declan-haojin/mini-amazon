from flask import current_app as app
from flask import url_for
from app.models.seller import Seller
class Product:
    """
    A product is anything that can be sold on the platform. It includes category information, price, description, image and other information
    """
    def __init__(self, product_id, category, image, name, description, price, available, created_by):
        """
        initialize a product object.
        """
        self.product_id = product_id
        self.category = category
        self.image = image
        self.name = name
        self.description = description
        self.price = price
        self.available = available
        self.created_by = created_by
        self.link = url_for('products.index', product_id=product_id)
        self.creator = Seller.get(created_by).name


    def __repr__(self):
        pass

    @staticmethod
    def get(product_id):
        """
        get a product that matches a given product id
        """
        rows = app.db.execute('''
            SELECT *
            FROM Products
            WHERE product_id = :id
            ''',
            id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        """
        get all products sorted by increasing price
        """
        rows = app.db.execute('''
            SELECT *
            FROM Products
            ORDER BY price ASC
        ''')
        return [Product(*row) for row in rows]

    @staticmethod
    def search_by_conditions(keywords, category, sort):
        """
        get products that match search conditions( filter by category, similar to a given string) ordered in ascending price
        """
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
        """
        Get all categories of products, we currently have categories like Technology, Books etc. 
        """
        rows = app.db.execute('''
            SELECT DISTINCT(category)
            FROM Products
        ''')
        return rows
    
    @staticmethod
    def get_count_by_categories():
        """
        Get count for products by category.  
        """
        rows = app.db.execute('''
            SELECT category,COUNT(*)
            FROM Products
            GROUP BY category
        ''')
        return rows

    @staticmethod
    def get_value_by_categories():
        """
        Get amount value for products by category.  
        """
        rows = app.db.execute('''
            SELECT category,SUM(price)
            FROM Products
            GROUP BY category
        ''')
        return rows

    @staticmethod
    def get_avgprice_by_categories():
        """
        Get average value for products by category.  
        """
        rows = app.db.execute('''
            SELECT category,CAST(AVG(price) AS DECIMAL)
            FROM Products
            GROUP BY category;
        ''')
        return rows

    @staticmethod
    def update(product_id, category, image, name, description, price, available):
        """
        Update product information including category, name, price etc.
        """
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
        """
        Create a new product that may not be available in the market.
        """
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
        # print(rows)
        return rows[0][0]

    @staticmethod
    def delete(product_id):
        """
        Delete a specific type of product in case it needs to be removed from the market.
        """
        app.db.execute('''
        DELETE FROM Products
        WHERE product_id = :product_id
        ''',
        product_id = product_id)
        return

    @staticmethod
    def get_k_most_expensive(k):
        """
        Get the k most expensive products. 
        """
        rows = app.db.execute('''
            SELECT product_id, name, price, available
            FROM Products
            ORDER BY price DESC
            LIMIT :k
            ''',
            k=k)
        return [Product(*row) for row in rows]
        
    @staticmethod
    def recommend(uid):
        """
        Get recommended products for given user based on most popular 
        50 products and top 3 categories the user has purchased from.
        """
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE Products.category IN (
            SELECT Products.category
            FROM Orders, Products
            WHERE uid = :uid
            AND Orders.product_id = Products.product_id
            GROUP BY Products.category
            ORDER BY COUNT(*) DESC
            LIMIT 3)
        AND Products.product_id IN (
            SELECT product_id
            FROM Orders
            GROUP BY product_id
            ORDER BY COUNT(*) DESC
            LIMIT 50
        )
        LIMIT 5
        ''',
        uid = uid)
        return [Product(*row) for row in rows]
