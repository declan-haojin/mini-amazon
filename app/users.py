from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,NumberRange
from flask import session

from .models.user import User
from .models.purchase import Purchase
from .models.order import Order
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.form.get('role') != None:
        print(request.form.get('role'))
        session['role'] = request.form.get('role')

    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.password.data)
        user = User.get_by_auth(form.email.data, form.password.data)
        # print(user)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        session['user'] = user.uid
        print(user.uid)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/user/profile', methods=['GET'])
def index():
    if current_user.is_authenticated:
        user = User.get(session['user'])
        purchases = []
        return render_template('user/index.html', user=user, purchases=purchases)
    else:
        return redirect(url_for('users.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            Seller.create(form.firstname.data,
                         form.lastname.data,
                         form.email.data,
                         form.password.data)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/user/hw4', methods=['GET'])
def getpurchases_hw4():
    uid = request.args.get('uid')
    if uid is None:
        purchases = []
    else:
        purchases = Order.get(uid)
    return render_template('hw4_user.html',purchases = purchases)

# @bp.route('/user/balance', methods=['GET', 'POST'])
# def balance_add():
#     user = User.get(session['user'])
#     User.topup_balance(user.id,100)
#     purchases = Purchase.get_by_uid(user.id)
#     print(purchases)
#     return render_template('user/index.html', user=user, purchases=purchases)

# @bp.route('/user/balance-add', methods=['GET', 'POST'])
# def balance_withdraw():
#     user = User.get(session['user'])
#     purchases = Purchase.get_by_uid(user.id)
#     User.withdraw_balance(user.id)
#     return render_template('user/index.html', user=user, purchases=purchases)


class CashForm(FlaskForm):
    amount = DecimalField('Deposit/ Withdraw Money', validators=[DataRequired(), NumberRange(min=0)])
    deposit = SubmitField('Add Money')
    withdraw = SubmitField('Withdraw Money')
    complete_withdraw = SubmitField('Withdraw Entire Amount')

@bp.route('/user/balance', methods=['GET', 'POST'])
def balances():
    form = CashForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            user = User.get(session['user'])
            if (form.deposit.data):
                User.topup_balance(user.id,form.amount.data)
            elif (form.withdraw.data):
                if (form.amount.data<=user.balance):
                    User.topup_balance(user.id,-form.amount.data)

            elif (form.complete_withdraw.data):
                User.withdraw_balance(user.id)
            return redirect(url_for('users.index'))
    else:
        return redirect(url_for('users.login'))
    return render_template('user/balance.html', title='My Account', form=form)

class UserForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat New Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Update my information')


@bp.route('/user/update', methods=['GET', 'POST'])
def update_profile():
    user = User.get(session['user'])
    if current_user.is_authenticated:
        form = UserForm()
        if form.validate_on_submit():
            if (User.email_exists):
                User.update(user.id,form.firstname.data,form.lastname.data,form.address.data,form.email.data,form.password.data)
            return redirect(url_for('users.index'))
    else:
        return redirect(url_for('users.login'))
    return render_template('user/details.html', title='My Account', form=form, user=user)
