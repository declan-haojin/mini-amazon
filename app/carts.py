from flask import render_template
from flask import request, flash, redirect, url_for
from .models.cart import Cart
from .models.order import Order
from .models.product import Product
from .models.user import User
from .models.inventory import Inventory
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

@bp.route('/cart/remove_item', methods=['POST'])
def remove_item():
    Cart.delete(request.args['uid'], request.args['seller_id'], request.args['product_id'])
    flash("The item has been deleted successfully")
    return redirect(url_for('carts.detail'))

@bp.route('/cart/add', methods=['GET', 'POST'])
def add():
    user_id = current_user.id
    seller_id = request.form['seller_id']
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    # print('***************************************')
    # print(user_id, seller_id, product_id)
    # print('***************************************')
    # If there's no this item in the cart
    current_item = Cart.get(user_id, seller_id, product_id)
    # print(current_item.product_name, current_item.seller_name)
    if current_item == None:
        # print('***************************************')
        Cart.create(user_id, seller_id, product_id, quantity)
    # Else we add 1 quantity to it
    else:
        Cart.update(user_id, seller_id, product_id, current_item.cart_quantity + quantity)

    flash("The product is added to the cart!")
    return redirect('/product/' + product_id)

@bp.route('/cart/submit', methods=['POST', 'GET'])
def submit():
    carts = Cart.get_all(uid=current_user.id)
    cart_total_price = 0
    for cart in carts:
        cart_total_price += cart.total_price

    # Check balance
    if current_user.balance < cart_total_price:
        flash("You don't have enough money for this purchase!")
        return redirect('/cart/detail')
    else:
        current_user.decrement_balance(cart_total_price)

    # Check inventory
    for cart in carts:
        curr_inventory = Inventory.get(seller_id=cart.seller_id, product_id=cart.product_id)
        if curr_inventory != None and curr_inventory.inventory_quantity >= cart.cart_quantity:
            Inventory.update(cart.seller_id, cart.product_id, curr_inventory.inventory_quantity - cart.cart_quantity)
        else:
            flash("There's not enough items left in the inventory!")
            return redirect('/cart/detail')

    # TODO: Create a new purchase here
    # TODO: For every cart, create a new order, add the order to the new purchase, add money to each seller, delete the cart
    # TODO: return to the new purchase history page

@bp.route('/cart/hw4', methods=['GET'])
def search():
    uid = request.args.get('uid')
    if uid is None:
        carts = []
    else:
        carts = Cart.get_all_by_uid(uid)
    return render_template('hw4_cart.html', carts = carts)
