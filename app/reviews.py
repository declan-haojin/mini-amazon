from flask import render_template
from flask import request, redirect
from .models.review import Review
from flask import session

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
        review_time = request.args.get('review_time')
        product_id = request.args.get('product_id')
        seller_id = Review.get_seller_id(uid, product_id)
        if seller_id == None: 
            return redirect('/review/search')
        else: 
            Review.create_product_review(uid, review_content, rating, review_time, seller_id, product_id)
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
        review_time = request.args.get('review_time')
        seller_id = request.args.get('seller_id')
        product_id = Review.get_product_id(uid, seller_id)
        review_content = request.args.get('review_content')
        Review.create_seller_review(uid, review_content, rating, review_time, seller_id, product_id)
        return redirect('/review/search')

@bp.route('/review/update', methods=['GET', 'POST'])
def update_review_page(): 
    if request.method == "GET":
        return render_template('reviews/update.html')
    else: 
        rating = request.args.get('rating')
        review_content = request.args.get('review_content')
        review_time = request.args.get('review_time')
        review_id = request.args.get('review_id')
        print(review_content)
        Review.update_review(review_id, review_content, review_time, rating)

        return redirect('/review/search')
        
