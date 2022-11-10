from flask import render_template
from flask import request
from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)

@bp.route('/review/search', methods=['GET'])
def search():
    uid = request.args.get('uid')
    if uid is None:
        reviews = []
    else:
        reviews = Review.get_all_by_uid(uid)
    return render_template('reviews/search.html', reviews=reviews)

@bp.route('/review/search_product', methods=['GET'])
def search_product_review():
    pid = request.args.get('product_id')
    if pid is None:
        reviews = []
    else:
        reviews = Review.get_all_by_pid(pid)
    return render_template('reviews/product_sum.html', reviews=reviews)

@bp.route('/review/search_seller', methods=['GET'])
def search_seller_review():
    sid = request.args.get('seller_id')
    if sid is None:
        reviews = []
    else:
        reviews = Review.get_all_by_sid(sid)
    return render_template('reviews/seller_sum.html', reviews=reviews)



@bp.route('/review/hw4', methods=['GET'])
def search_hw4():
    uid = request.args.get('uid')
    if uid is None:
        reviews = []
    else:
        reviews = Review.get_5_most_recent(uid)
    return render_template('hw4_review.html', reviews=reviews)


@bp.route('/review/product', methods=['GET'])
def insert_product_review():
    uid = request.args.get('uid')
    if not uid: 
        uid = "-1"
        review_content = "-1"
        rating = "-1"
        review_time = "-1" 
        seller_id = "-1" 
        product_id = "-1"
        
    else: 
        review_content = request.args.get('review_content')
        rating = request.args.get('rating')
        review_time = request.args.get('review_time')
        seller_id = request.args.get('seller_id')
        product_id = request.args.get('product_id')
        Review.create_product_review(uid,review_content, rating, review_time, seller_id, product_id)

    return render_template('reviews/product_review_submission.html')

@bp.route('/review/seller', methods=['GET'])
def insert_seller_review():
    uid = request.args.get('uid')
    if not uid: 
        uid = "0"
        review_content = "-1"
        rating = "-1"
        review_time = "2022-11-09"
        seller_id = "0" 
        product_id = "0"
    else: 
        content = request.args.get('review_content')
        rating = request.args.get('rating')
        review_time = request.args.get('review_time')
        seller_id = request.args.get('seller_id')
        product_id = request.args.get('product_id')

    Review.create_seller_review(uid,review_content, rating, review_time, seller_id, product_id)

    return render_template('reviews/seller_review_submission.html')