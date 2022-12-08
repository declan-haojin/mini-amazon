from flask import render_template
from flask import request, flash, redirect, url_for
from .models.cart import Cart
from .models.order import Order
from .models.product import Product
from .models.user import User
from .models.seller import Seller
from .models.purchase import Purchase
from .models.inventory import Inventory
from flask import session
from flask_login import current_user
from datetime import datetime
from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/cart/order', methods=['GET'])
def order():
    if current_user.is_authenticated:
        return render_template('carts/detailedorder.html')
    else:
        return redirect(url_for('users.login'))


@bp.route('/cart/detail', methods=['GET', 'POST'])
def detail():
 if current_user.is_authenticated:
    if request.method == 'POST':
        # print(request.form['uid'])
        Cart.update(request.form['uid'], request.form['seller_id'], request.form['product_id'], request.form['cart_quantity'])
        flash("The item quantity has been updated successfully")
        return redirect(url_for('carts.detail'))

    carts = Cart.get_all(uid=current_user.id)
    cart_total_price = 0
    for cart in carts:
        cart_total_price += cart.total_price
    products = Inventory.recommend(current_user.id) #recommendation based on: 1. the users top 3 purchasing categories, 2. the product must be top 50 popular
    return render_template('carts/detail.html', carts = carts, cart_total_price = cart_total_price, productlist = products)
 else:
        return redirect(url_for('users.login'))
@bp.route('/cart/remove_item', methods=['POST'])
def remove_item():
    if current_user.is_authenticated:
        Cart.delete(request.args['uid'], request.args['seller_id'], request.args['product_id'])
        flash("The item has been deleted successfully")
        return redirect(url_for('carts.detail'))
    else:
        return redirect(url_for('users.login'))

@bp.route('/cart/add', methods=['GET', 'POST'])
def add():
    if not current_user.is_authenticated:
        return redirect('/login')
    if session['role'] == 'seller':
        flash("Please login as a buyer and try again!")
        return redirect('/')
    user_id = current_user.id
    seller_id = request.form['seller_id']
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    print("user_id seller_id product_id", user_id, seller_id, product_id)
    current_item = Cart.get(user_id, seller_id, product_id)
    # print("user_Id", user_id)
    # print(current_item.product_name, current_item.seller_name)
    if current_item == None:
        Cart.create(user_id, seller_id, product_id, quantity)
    # Else we add 1 quantity to it
    else:
        # print('Quantity', quantity)
        # print('current_item.cart_quantity', current_item.cart_quantity)
        # print('sum', current_item.cart_quantity + quantity)
        # print("####", user_id, seller_id, product_id, current_item.cart_quantity + quantity)
        Cart.update(user_id, seller_id, product_id, current_item.cart_quantity + quantity)

    flash("The product is added to the cart!")
    return redirect('/product/' + product_id)

@bp.route('/cart/submit', methods=['POST', 'GET'])
def submit():
    if not (current_user.is_authenticated and session['role'] == 'buyer'):
        return redirect('/login')
    carts = Cart.get_all(uid=current_user.id)

    if carts == []:
        flash("You don't have anything in the cart!")
        return redirect('/cart/detail')

    cart_total_price = 0
    for cart in carts:
        cart_total_price += cart.total_price

    # If the user enter the correct coupon code
    if request.form.get('coupon') == 'CHECKOUT10':
        cart_total_price=0.9*int(cart_total_price)

    # Check balance
    if current_user.balance < cart_total_price:
        diff=str(cart_total_price-current_user.balance)
        flash("You don't have enough money for this purchase! Add $"+diff+" to complete current purchase!" )
        return redirect('/cart/detail')
    else:
        User.topup_balance(current_user.id,-cart_total_price)

    # Check inventory
    for cart in carts:
        curr_inventory = Inventory.get(seller_id=cart.seller_id, product_id=cart.product_id)
        if curr_inventory == None or curr_inventory.inventory_quantity < cart.cart_quantity:
            flash("There's not enough "+cart.product_name+" left in the inventory for this seller!")
            return redirect('/cart/detail')

    # Create Purchase, Update inventory
    new_purchase = Purchase.create_purchase(current_user.id, len(carts), cart_total_price, "Processing")
    for cart in carts:
        # Decrement seller inventory
        curr_inventory = Inventory.get(seller_id=cart.seller_id, product_id=cart.product_id)
        Inventory.update(cart.seller_id, cart.product_id, curr_inventory.inventory_quantity - cart.cart_quantity)
        # Increment seller balance
        Seller.topup_balance(cart.seller_id, cart.total_price)
        # Create order for this purchase
        Order.create(current_user.id, new_purchase.purchase_id, cart.cart_quantity,cart.total_price,"Processing",cart.product_id, cart.seller_id)
        # Delete this line of cart
        Cart.delete(cart.uid, cart.seller_id, cart.product_id)

    if request.form.get('coupon') == 'CHECKOUT10':
        flash("Coupon is valid and used!")
    return redirect(url_for('purchases.index', purchase_id=new_purchase.purchase_id))

@bp.route('/cart/hw4', methods=['GET'])
def search():
    if not (current_user.is_authenticated and session['role'] == 'buyer'):
        return redirect('/login')
    uid = request.args.get('uid')
    if uid is None:
        carts = []
    else:
        carts = Cart.get_all_by_uid(uid)
    return render_template('hw4_cart.html', carts = carts)
