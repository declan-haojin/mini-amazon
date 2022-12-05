from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.order import Order

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    print(Order.update(6,42,199,"Processing"))
    # get all available products for sale:
    # products = Product.get_all(True)
    # purchases = []
    # find the products current user has bought:
    # if current_user.is_authenticated:
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # else:
    #     purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html')
