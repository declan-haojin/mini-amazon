from flask import render_template
from flask import request, redirect
from .models.cart import Cart
from .models.product import Product
from flask import session

from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/cart/order', methods=['GET'])
def order():
    return render_template('carts/order.html')

@bp.route('/cart/detail', methods=['GET', 'POST'])
def detail():
    if request.method == "POST":
        Cart.remove_item(request.form['delete'])
        return redirect('/cart/detail')
    else:
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