from flask import render_template
from flask import request, redirect, flash
from .models.review import Review
from flask import session, url_for
from datetime import datetime

from flask import Blueprint
bp = Blueprint('reviews', __name__)

@bp.route('/review/search', methods=['GET', 'POST'])
def search():
    if request.form.get('delete'):
        Review.remove_review(request.form.get('delete'))
        return redirect('/review/search')
    else:
        reviews = Review.get_all_by_uid(session["user"])
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
    uid = session["user"]
    rating = request.args.get('rating')
    if not rating:
        return render_template('reviews/product_review_submission.html')
    else:
        review_content = request.args.get('review_content')
        review_time = datetime.now()
        product_id = request.args.get('product_id')
        if Review.existProduct(uid): 
            seller_id = Review.get_seller_id(uid, product_id)
        
        # if a user hasn't bought this product
        if seller_id == 0: 
            flash("You haven't bought this product")
            return redirect('/review/product')
        else: 
            exist = Review.create_product_review(uid, review_content, rating, review_time, seller_id, product_id)
            # if a review already exists for a product
            if exist: flash("You can only submit one review for each product you bought from this seller")
            return redirect('/review/search')

@bp.route('/review/product/submit_link/', methods=['GET'])
def submit_link():
    print("Thank you for your review!")
    return "Click." 

@bp.route('/review/seller', methods=['GET'])
def insert_seller_review():
    uid = session["user"]
    rating = request.args.get('rating')
    if not rating:
        return render_template('reviews/seller_review_submission.html')
    else:
        content = request.args.get('review_content')
        review_time = datetime.now()
        seller_id = request.args.get('seller_id')
        product_id = Review.get_product_id(uid, seller_id)
        if product_id == 0: 
            flash("You haven't bought any product from this seller")
            return redirect('/review/seller')
        review_content = request.args.get('review_content')
        exist = Review.create_seller_review(uid, review_content, rating, review_time, seller_id, product_id)
        if exist: flash("You can only submit one review for each product you bought from this seller")
        return redirect('/review/search')

@bp.route('/review/update', methods=['GET', 'POST'])
def update_review_page(): 
    if request.method == "GET":
        return render_template('reviews/update.html')
    else: 
        review_id = request.args.get('review_id')
        rating = request.form['rating']
        review_content = request.form['review_content']
        review_time = datetime.now()
        Review.update_review(review_id, review_content, review_time, rating)

        return redirect('/review/search')
        
@bp.route('/review/vote', methods=['GET', 'POST'])
def vote():
    review_id = request.args['review_id']
    Review.update_vote(review_id)
    sid = request.args['sid']
    return redirect(url_for('seller.index', sid=sid))