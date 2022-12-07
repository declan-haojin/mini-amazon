from flask import render_template, flash
from flask import request, redirect, session
from flask_login import current_user
from .models.product import Product
from .models.review import Review
from .models.inventory import Inventory
from .models.seller import Seller
from .models.order import Order
from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('purchases', __name__)

@bp.route('/purchase/<purchase_id>', methods=['GET', 'POST'])
def index(purchase_id):
    purchase = Purchase.get_by_purchase_id(purchase_id)
    print(purchase)
    if current_user.is_authenticated and purchase.uid == current_user.id:
        return render_template('purchase/index.html', purchase=purchase, orders=purchase.get_orders())
    flash("You do not have access to this order!")
    return redirect('/login')



@bp.route('/purchase/search', methods=['GET'])
def search():
    # If there's no search input, display all the products
    if request.args == {}:
        purchases = Purchase.get_by_uid(session['user'])
    else:
        start = request.args.get('start')
        end = request.args.get('end')
        keywords = request.args.get('keywords')
        purchases = Purchase.search_by_conditions(session['user'],start, end, keywords)

    return render_template('purchase/search.html', purchases = purchases)