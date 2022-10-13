from flask import render_template
from flask import request
from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)



@bp.route('/product/hw4', methods=['GET'])
def find_k_most_expensive():
    return render_template('hw4_product.html')
    products = Product.get_k_most_expensive(2)
    return render_template('hw4_product.html')

