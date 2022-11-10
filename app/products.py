from flask import render_template
from flask import request
from .models.product import Product

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


@bp.route('/product/<product_id>', methods = ['GET'])
def index(product_id):
    if product_id is None:
        product = None
    else:
        product = Product.get(product_id)
        # print(product)
    return render_template('products/index.html', product = product)


@bp.route('/product/hw4', methods=['GET'])
def search_hw4():
    k = request.args.get('k')
    if k is None:
        products = []
    else:
        products = Product.get_k_most_expensive(k)
    return render_template('hw4_product.html', products = products)
