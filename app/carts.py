from flask import render_template
from flask import request
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/cart/hw4', methods=['GET'])
def search():
    uid = request.args.get('uid')
    if uid is None:
        carts = []
    else:
        carts = Cart.get_all_by_uid(uid)
    return render_template('hw4_cart.html', carts = carts)

