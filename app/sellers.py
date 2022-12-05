from flask import render_template
from flask import request, redirect
from .models.inventory import Inventory
from .models.seller import Seller
from .models.product import Product
from .models.review import Review
from flask_login import login_user, logout_user, current_user

from flask import session

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/<sid>', methods = ['GET'])
def index(sid):
    if sid is None:
        products = []
        names = []
        reviews = []
        avg_rating = 0
        num_rating = 0
    else:
        products = Inventory.get_by_sid(sid)
        seller = Seller.get_seller_object(sid)
        reviews = Review.get_all_by_sid(sid)
        avg_rating, num_rating = Review.sum_seller_review(sid)
    return render_template('seller/seller_index.html', products = products, seller = seller, reviews = reviews, avg_rating = avg_rating, num_rating = num_rating)

@bp.route('/seller/search', methods=['GET'])
def sellers_search():
    if not current_user.is_authenticated:
        return redirect('/login')
    sid = session['user']
    seller = Seller.get_seller_object(sid)
    if sid is None:
        products = []
    else:
        products = Inventory.get_by_sid(sid)
    if products is None:
        products = []
    return render_template('seller/seller_search.html', products = products, seller = seller)

@bp.route('/seller/add', methods=['GET'])
def sellers_add():
    if not current_user.is_authenticated:
        return redirect('/login')
    sid = session['user']
    pid = request.args.get('pid')
    qty = request.args.get('qty')
    if request.args == {}:
        args = "No Status"
    else:
        args = Inventory.add_item_to_inventory(sid, pid, qty)
    return render_template('seller/seller_add.html', args = args)

@bp.route('/seller/fulfill/', methods = ['GET', 'POST'])
def sellers_fulfill():
    if not current_user.is_authenticated:
        return redirect('/login')
    sid = session['user']
    if request.form.get('order_id') != None:
        oid = request.form.get('order_id')
        status = Inventory.get_status(oid)
        if status[0][0]!= "Processing": print("NOT VALID")
        else:
            status = "Confirmed"
            Inventory.change_order_status_spc(oid,status)
        return redirect('/seller/fulfill/')
    else:
        args = Inventory.get_order(sid)
        retlist = []
        for arg in args:
            newarg = []
            newarg.append(arg[0])
            newarg.append(arg[1])
            newarg.append(arg[2])
            newarg.append(arg[3])
            newarg.append(arg[4])
            newarg.append(arg[5])
            if "Delivered" in arg[6] : newarg.append("Delivered")
            elif "Out for Delivery" in arg[6] : newarg.append("Out for Delivery")
            elif "Confirmed" in arg[6] : newarg.append("Confirmed")
            elif "Processing" in arg[6] : newarg.append("Processing")
            retlist.append(newarg)
            Inventory.change_order_status_spc(newarg[4], newarg[6])
        return render_template('seller/seller_fulfill.html', args = retlist)
