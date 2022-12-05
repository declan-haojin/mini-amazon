from flask import render_template
from flask import request, flash, redirect
from .models.cart import Cart
from .models.product import Product
from flask import session
from flask_login import current_user

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


# @bp.route('/cart/quantity', methods=['GET', 'POST'])
# def update_quantity():
#     if request.method == "GET":
#         return render_template('carts/quantity.html')
#     else:
#         product_id = request.args.get('product_id')
#         Cart.update_quantity(request.form['save'], product_id)
#         return redirect('/cart/detail')


# @bp.route('/cart/add', methods=['POST'])
# def add():
#     cart_quantity = request.args.get('cart_quantity')
#     product_id = request.args.get('product_id')
#     Cart.update_quantity(product_id, cart_quantity)


@bp.route('/cart/add', methods=['GET'])
def add():
    user_id = current_user.id
    seller_id = request.args['seller_id']
    product_id = request.args['product_id']

    # If there's no this item in the cart
    if Cart.get(user_id, seller_id, product_id) == None:
        Cart.create(user_id, seller_id, product_id, 1, Product.get(product_id))
    # Else we add 1 quantity to it
    else:
        Cart.update_quantity(user_id, seller_id, product_id, 1)

    flash("The product is added to the cart!")
    return redirect('/product/' + request.args['product_id'])

    # carts = Cart.get_all(uid=session['user'], quantity=0)
    # return render_template('carts/detail.html', carts = carts)

@bp.route('/cart/hw4', methods=['GET'])
def search():
    uid = request.args.get('uid')
    if uid is None:
        carts = []
    else:
        carts = Cart.get_all_by_uid(uid)
    return render_template('hw4_cart.html', carts = carts)
