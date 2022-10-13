from flask import render_template
import datetime

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)




@bp.route('/product/hw4', methods=['GET', 'POST'])
def find_k_most_expensive():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)
