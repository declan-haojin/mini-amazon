from flask import render_template
from flask import request
from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/product/search', methods=['GET'])
def search():
    products = []
    return render_template('products/search.html', products = products)


@bp.route('/product/hw4', methods=['GET'])
def search_hw4():
    k = request.args.get('k')
    if k is None:
        products = []
    else:
        products = Product.get_k_most_expensive(k)
    return render_template('hw4_product.html', products = products)

