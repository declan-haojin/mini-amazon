from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB



login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .products import bp as product_bp
    app.register_blueprint(product_bp)

    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .sellers import bp as seller_bp
    app.register_blueprint(seller_bp)

    from .reviews import bp as review_bp
    app.register_blueprint(review_bp)

    from .orders import bp as order_bp
    app.register_blueprint(order_bp)

    from .purchases import bp as purchases_bp
    app.register_blueprint(purchases_bp)

    return app
