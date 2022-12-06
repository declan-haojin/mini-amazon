from flask import render_template, flash
from flask import request, redirect, session
from .models.product import Product
from .models.review import Review
from .models.inventory import Inventory
from .models.seller import Seller
from .models.order import Order


from flask import Blueprint
bp = Blueprint('orders', __name__)

@bp.route('/order/<order_id>', methods=['GET', 'POST'])
def index(order_id):
    return render_template('orders/index.html', order = Order.get(order_id))
