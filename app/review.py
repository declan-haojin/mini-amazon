from flask import render_template
from flask import request
from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)



@bp.route('/review/hw4', methods=['GET'])
def search():
    k = 5
    reviews = Review.get_k_most_expensive(k)
    return render_template('hw4_social.html', reviews = reviews)

