from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.order import Order
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # print(Cart.get(0, 0, 1).product_id)
    # print(Order.get_by_purchase_id(72))
    # print(Order.create(1, 72, 1, 10, "Confirmed", 0).order_id)
    # Purchase.get_by_purchase_id(40).add_order(100)
    # print(current_user.decrement_balance(10))
    # print(Inventory.update(0, 3, 1000).inventory_quantity)
    # print(Order.get(0))
    # Cart.delete(0, 1, 92)
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
