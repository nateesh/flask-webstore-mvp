from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Category, Book, Order
from datetime import datetime
from sqlalchemy import or_
from .forms import CheckoutForm  # , ShippingChoice
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    books = Book.query.order_by(Book.name).all()

    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None

    cats = Category.query.order_by(Category.id).all()
    return render_template('index.html', page='index', cats=cats, books=books, order=order)


@bp.route('/category/<int:cat_id>')
def category(cat_id):
    category = Category.query.get_or_404(cat_id)
    cats = Category.query.order_by(Category.id).all()

    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None

    books = Book.query.filter_by(category_id=cat_id).all()
    return render_template('category.html', category=category, books=books, cats=cats, order=order)


@bp.route('/book/<int:bookid>/')
def bookinfo(bookid):

    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None

    book = Book.query.get_or_404(bookid)
    cats = Category.query.order_by(Category.id).all()
    return render_template('product.html', book=book, cats=cats, order=order)


@bp.route('/book/')
def search():
    search = {'search': request.args.get('search')}

    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None
    print(search)
    if search['search'] == '':
        flash("You didn't enter anything to search for, so we're showing you all our available books.")

    books = Book.query.filter(or_(Book.description.ilike('%' + search['search'] + '%'),
                                  Book.short_desc.ilike(
                                      '%' + search['search'] + '%'),
                                  Book.name.ilike(
                                      '%' + search['search'] + '%'),
                                  Book.author.ilike('%' + search['search'] + '%'))).all()

    cats = Category.query.order_by(Category.id).all()
    return render_template('index.html', cats=cats, books=books, order=order)


# Referred to as "Basket" to the user


@bp.route('/order', methods=['POST', 'GET'])
def order():
    cats = Category.query.order_by(Category.id).all()
    book_id = request.values.get('book_id')
    books = Book.query.order_by(Book.name).all()

    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status=False, first_name='', last_name='',
                      email='', phone='', total_cost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None

    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for book in order.books:
            totalprice = totalprice + book.price

    # are we adding an item?
    if book_id is not None and order is not None:
        book = Book.query.get(book_id)
        if book not in order.books:
            try:
                order.books.append(book)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket!'
            return redirect(url_for('main.order'))
        else:
            flash('This book is already in your basket!')
            return redirect(url_for('main.order'))

    # checkout business logic
    # shipping = ShippingChoice(request)
    # testing = shipping

    form = CheckoutForm()
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])

        if form.validate_on_submit():
            order.status = True
            order.first_name = form.first_name.data
            order.last_name = form.first_name.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for book in order.books:
                totalcost = totalcost + book.price
            order.total_cost = totalcost
            order.date = datetime.now()
            if totalcost == 0:
                flash("You have no items in your basket, so we couldn't process your order!")
                return redirect(url_for('main.order'))
            else:
                try:
                    db.session.commit()
                    del session['order_id']
                    flash(
                        'Thank you for your order! We look forward to selling you more books in the future :)')
                    return redirect(url_for('main.index'))
                except:
                    return 'There was an issue completing your order'

    return render_template('order.html', order=order, totalprice=totalprice, cats=cats,
                           books=books, form=form)


# Delete specific basket items
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        Book_to_delete = Book.query.get(id)
        try:
            order.books.remove(Book_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))
