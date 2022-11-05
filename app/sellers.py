from flask import render_template
from flask import request
from .models.inventory import Inventory
from .models.product import Product

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/hw4', methods=['GET'])
def sellers_hw4():
    sid = request.args.get('sid')
    if sid is None:
        products = []
    else:
        products = Inventory.get_by_sid(sid)

        
    return render_template('hw4_seller.html', products = products)

@bp.route('/seller/add', methods=['GET'])
def sellers_add():
    sid = request.args.get('sid')
    pid = request.args.get('pid')
    qty = request.args.get('qty')
    arg = Inventory.add_item_to_inventory(sid, pid, qty)
    return render_template('seller_add.html', arg = arg)