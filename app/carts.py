from flask import render_template
from flask import request
from .models.cart import Cart
from .models.product import Product
from flask import session

from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/cart/order', methods=['GET'])
def order():
    return render_template('carts/order.html')

@bp.route('/cart/detail', methods=['GET'])
def detail():
    carts = Cart.get_all(uid=session['user'], quantity=0)
    return render_template('carts/detail.html', carts = carts)


@bp.route('/cart/hw4', methods=['GET'])
def search():
    uid = request.args.get('uid')
    if uid is None:
        carts = []
    else:
        carts = Cart.get_all_by_uid(uid)
    return render_template('hw4_cart.html', carts = carts)
