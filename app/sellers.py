from flask import render_template
from flask import request
from .models.inventory import Inventory
from .models.seller import Seller
from .models.product import Product

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/<sid>', methods = ['GET'])
def index(sid) :
    if sid is None:
        products = []
        names = []
    else:
        products = Inventory.get_by_sid(sid)
        names = Seller.get_by_sid(sid)

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
