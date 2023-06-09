from flask import render_template
from flask import request, redirect, url_for, flash

from app.models.order import Order
from .models.inventory import Inventory
from .models.seller import Seller
from .models.product import Product
from .models.review import Review
from flask_login import login_user, logout_user, current_user

from flask import session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,NumberRange

from datetime import date

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/<sid>', methods = ['GET'])
def index(sid):
    if sid is None:
        products = []
        reviews = []
        avg_rating = 0
        num_rating = 0
    else:
        products = Inventory.get_by_sid(sid)
        seller = Seller.get(sid)
        reviews = Review.get_all_by_sid(sid)
        avg_rating, num_rating = Review.sum_seller_review(sid)
    return render_template('seller/seller_index.html', products = products, seller = seller, reviews = reviews, avg_rating = avg_rating, num_rating = num_rating)

@bp.route('/seller/search', methods=['GET', 'POST'])
def sellers_search():
    if not current_user.is_authenticated: #every time, check autentication
        return redirect('/login')
    if request.form.get('pid') != None: #delete button is clicked
        pid = request.form.get('pid')
        Inventory.delete(pid)
        return redirect(url_for('seller.sellers_search'))
    sid = session['user']
    seller = Seller.get(sid)
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
        args = "No Status" #args as a string
    else:
        args = Inventory.add_item_to_inventory(sid, pid, qty) #return a string
    return render_template('seller/seller_add.html', args = args)

@bp.route('/seller/fulfill/', methods = ['GET', 'POST'])
def sellers_fulfill():
    if not current_user.is_authenticated:
        return redirect('/login')
    sid = session['user']
    if request.form.get('order_id') != None: #fulfill button is clicked
        oid = request.form.get('order_id')
        status = Inventory.get_status(oid)
        if status[0][0]!= "Processing": flash("This order is already fulfilled")
        else:
            status = "Fulfilled"
            Inventory.change_order_status_spc(oid,status)
        return redirect('/seller/fulfill/')
    else:
        args = Order.get_by_seller_id(sid)
        retlist = []
        for arg in args:
            newarg = [] #manually add elements in the list from legacyrow object
            newarg.append(arg[0])
            newarg.append(arg[1])
            newarg.append(arg[2])
            newarg.append(arg[3])
            newarg.append(arg[4])
            newarg.append(arg[5])
            if "Fulfilled" in arg[6] : newarg.append("Fulfilled") #make sure status only exists as string and is updated
            elif "Processing" in arg[6] : newarg.append("Processing")
            retlist.append(newarg)
            Inventory.change_order_status_spc(newarg[4], newarg[6])
        return render_template('seller/seller_fulfill.html', args = retlist)

@bp.route('/seller/analytics', methods = ['GET'])
def analytics():
    if not current_user.is_authenticated:
        return redirect('/login')
    sid = session['user']
    start = request.args.get('start')
    end = request.args.get('end')
    if start == '':
        start = "1999-01-01"
    if end == '':
        end = date.today() #check if inputs are empty strings
    count = Inventory.get_analytics_category(sid)
    pop = Inventory.get_analytics_order(sid, start, end)
    users= Review.get_analytics_user(sid)
    return render_template('seller/seller_analytics.html', count = count, pop = pop, users = users)

class UserForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField('Update my information')

@bp.route('/seller/update', methods=['GET', 'POST'])
def update_profile():
    seller = Seller.get(session['user'])
    if current_user.is_authenticated:
        form = UserForm()
        if form.validate_on_submit():
            if (seller.email_exists):
                seller.update(seller.id,form.firstname.data,form.lastname.data,form.address.data)
            return redirect(url_for('seller.sellers_search'))
    else:
        return redirect(url_for('users.login'))
    return render_template('seller/seller_detail.html', title='My Account', form=form, user=seller)


class CashForm(FlaskForm):
    amount = DecimalField('Deposit/ Withdraw Money', validators=[DataRequired(), NumberRange(min=0, max=999999999)])
    deposit = SubmitField('Add Money')
    withdraw = SubmitField('Withdraw Money')
    complete_withdraw = SubmitField('Withdraw Entire Amount')

@bp.route('/seller/balance', methods=['GET', 'POST'])
def balances():
    form = CashForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            seller = Seller.get(session['user'])
            if (form.deposit.data):
                Seller.topup_balance(seller.id,form.amount.data)
            elif (form.withdraw.data):
                if (form.amount.data<=seller.balance):
                    seller.topup_balance(seller.id,-form.amount.data)

            elif (form.complete_withdraw.data):
                Seller.withdraw_balance(seller.id)
            return redirect(url_for('seller.sellers_search'))
    else:
        return redirect(url_for('users.login'))
    return render_template('user/balance.html', title='My Account', form=form)