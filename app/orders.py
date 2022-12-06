from flask import render_template, flash
from flask import request, redirect, session
from flask_login import current_user
from .models.product import Product
from .models.review import Review
from .models.inventory import Inventory
from .models.seller import Seller
from .models.order import Order


from flask import Blueprint
bp = Blueprint('orders', __name__)

@bp.route('/order/<order_id>', methods=['GET', 'POST'])
def index(order_id):
    order = Order.get(order_id)
    if current_user.is_authenticated and order.uid == current_user.id:
        return render_template('orders/index.html', order = order)
    flash("You do not have access to this order!")
    return redirect('/login')
