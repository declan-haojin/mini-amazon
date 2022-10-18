from flask import render_template
from flask import request
from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)

@bp.route('/review/search', methods=['GET'])
def search():
    reviews = []
    return render_template('reviews/search.html', reviews=reviews)


@bp.route('/reviews/hw4', methods=['GET'])
def search_hw4():
    k = request.args.get('k')
    uid = request.args.get('uid')
    if k is None:
        reviews = []
    else:
        reviews = Review.get_k_most_recent(k, uid)
    return render_template('hw4_review.html', reviews=reviews)