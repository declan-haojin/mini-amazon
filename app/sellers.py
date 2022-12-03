from flask import render_template
from flask import request
from .models.inventory import Inventory
from .models.seller import Seller
from .models.product import Product
from .models.review import Review

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/<sid>', methods = ['GET'])
def index(sid) :
    if sid is None:
        products = []
        names = []
        reviews = []
        avg_rating = 0
        num_rating = 0
    else:
        products = Inventory.get_by_sid(sid)
        names = Seller.get_by_sid(sid)
        reviews = Review.get_all_by_sid(sid)
        avg_rating, num_rating = Review.sum_seller_review(sid)

    return render_template('seller/seller_index.html', products = products, sid = sid, names = names)

@bp.route('/seller/search', methods=['GET'])
def sellers_search():
    sid = request.args.get('sid')
    if sid is None:
        products = []
    else:
        products = Inventory.get_by_sid(sid)
    if products is None:
        products = []
    return render_template('seller/seller_search.html', products = products)

@bp.route('/seller/add', methods=['GET'])
def sellers_add():
    sid = request.args.get('sid')
    pid = request.args.get('pid')
    qty = request.args.get('qty')
    if request.args == {}:
        args = "No Status"
    else:
        args = Inventory.add_item_to_inventory(sid, pid, qty)
    return render_template('seller/seller_add.html', args = args)

@bp.route('/seller/fulfill/<sid>', methods = ['GET', 'POST'])
def sellers_fulfill(sid):
    
    if sid is None:
        return
    args = Inventory.get_order(sid)

    return render_template('seller/seller_fulfill.html', args = args)