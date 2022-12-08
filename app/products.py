from flask import render_template, flash
from flask import request, redirect, session
from .models.product import Product
from .models.review import Review
from .models.inventory import Inventory
from .models.seller import Seller
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.route('/product/search', methods=['GET'])
def search():
    # If there's no search input, display all the products
    if request.args == {}:
        products = Product.get_all()
    else:
        keywords = request.args.get('keywords')
        category = request.args.get('category')
        sort = request.args.get('sort')
        products = Product.search_by_conditions(keywords=keywords, category=category, sort=sort)

    return render_template('products/search.html', products = products)

@bp.route('/product/list', methods = ['GET'])
def list():
    return render_template('products/list.html')

@bp.route('/product/<product_id>', methods = ['GET'])
def index(product_id):
    if product_id is None:
        product = None
        reviews = None
        avg_rating = 0
        num_rating = 0
    else:
        product = Product.get(product_id)
        reviews = Review.get_all_by_pid(product_id)
        sellerid_quantity = Inventory.get_by_pid(product_id)
        sellers = []

        for seller in sellerid_quantity:
            seller_id = seller['seller_id']
            quantity = seller['inventory_quantity']
            first_lastname = Seller.get_by_sid(seller_id)
            seller_name = first_lastname['firstname'] + " " + first_lastname['lastname']
            sellers.append([seller_name, quantity, str(seller_id)])

        avg_rating, num_rating = Review.sum_product_review(product_id)
    return render_template('products/index.html', product = product, reviews = reviews, avg_rating = avg_rating, num_rating = num_rating, sellers = sellers, is_creator = (session['user'] == product.created_by))


@bp.route('/product/<product_id>/edit', methods=['GET', 'POST'])
def edit(product_id):
    if request.method == 'GET':
        return render_template('products/edit.html', product = Product.get(product_id))
    else:
        Product.update(
            product_id=product_id,
            category=request.form['category'],
            image=request.form['image'],
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            available=request.form['available']
        )
        return redirect('/product/' + product_id)

@bp.route('/product/create', methods=['GET', 'POST'])
def create():
    # Check if any input is empty
    for arg in request.form:
        if len(request.form[arg]) == 0:
            flash("Your input is invalid")
            return redirect('/product/create')

    if request.method == 'GET':
        return render_template('products/create.html')
    else:
        product_id = Product.create(
            category=request.form['category'],
            image=request.form['image'],
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            available=request.form['available'],
            created_by=session['user']
        )
        return redirect('/product/' + str(product_id))

@bp.route('/product/<product_id>/delete', methods=['GET'])
def delete(product_id):
    Product.delete(product_id=product_id)
    flash('The product has been deleted successfully!')
    return redirect('/product/search')


@bp.route('/product/hw4', methods=['GET'])
def search_hw4():
    k = request.args.get('k')
    if k is None:
        products = []
    else:
        products = Product.get_k_most_expensive(k)
    return render_template('hw4_product.html', products = products)
