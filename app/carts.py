from flask import render_template
from flask import request, flash, redirect, url_for
from .models.cart import Cart
from .models.product import Product
from flask import session
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/cart/order', methods=['GET'])
def order():
    return render_template('carts/detailedorder.html')

@bp.route('/cart/detail', methods=['GET', 'POST'])
def detail():
    if request.method == 'POST':
        # print(request.form['uid'])
        Cart.update(request.form['uid'], request.form['seller_id'], request.form['product_id'], request.form['cart_quantity'])
        flash("The item quantity has been updated successfully")
        return redirect(url_for('carts.detail'))

    carts = Cart.get_all(uid=current_user.id)
    cart_total_price = 0
    for cart in carts:
        cart_total_price += cart.total_price

    return render_template('carts/detail.html', carts = carts, cart_total_price = cart_total_price)

# @bp.route('/cart/update_item', methods=['POST'])
# def update_item():
#     Cart.update(request.args['uid'], request.args['seller_id'], request.args['product_id'], request.args['cart_quantity'])
#     flash("The item quantity has been updated successfully")
#     return redirect(url_for('carts.detail'))

@bp.route('/cart/remove_item', methods=['POST'])
def remove_item():
    Cart.delete(request.args['uid'], request.args['seller_id'], request.args['product_id'])
    flash("The item has been deleted successfully")
    return redirect(url_for('carts.detail'))

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


@bp.route('/cart/add', methods=['GET', 'POST'])
def add():
    user_id = current_user.id
    seller_id = request.form['seller_id']
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    print(request.form)
    # If there's no this item in the cart
    current_item = Cart.get(user_id, seller_id, product_id)
    if current_item == None:
        Cart.create(user_id, seller_id, product_id, quantity)
    # Else we add 1 quantity to it
    else:
        Cart.update(user_id, seller_id, product_id, current_item.cart_quantity + quantity)

    flash("The product is added to the cart!")
    return redirect('/product/' + product_id)

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
