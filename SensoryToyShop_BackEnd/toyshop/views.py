from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Product, Order, ProductCategory, ProductInfo
from datetime import datetime
from .forms import CheckoutForm
from . import db

bp = Blueprint('main', __name__)


# Index
@bp.route('/')
def index():
    productCategories = ProductCategory.query.order_by(
        ProductCategory.name).all()
    return render_template('index.html', productCategories=productCategories)


# Product Category
@bp.route('/products/<int:productCategoryid>')
def productCategory(productCategoryid):
    products = Product.query.filter(
        Product.productCategory_id == productCategoryid)
    return render_template('productCategories.html', products=products)


# Product Info
@bp.route('/product/<int:productid>')
def productInfo(productid):
    product = Product.query.filter(Product.id == productid).one()
    productInfo = ProductInfo.query.filter(
        ProductInfo.product_id == productid).one()
    return render_template('productInfo.html', productInfo=productInfo, product=product)


# Referred to as "Cart" to the user
# Order

@bp.route('/order', methods=['POST', 'GET'])
def order():
    product_id = request.values.get('product_id')

    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # if there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status=False, firstname='', surname='',
                      email='', phone='', totalcost=0, date=datetime.now())
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
        for product in order.products:
            totalprice = totalprice + product.price

    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your cart'
            return redirect(url_for('main.order'))
        else:  # if user attempts to add an item that already exists in cart
            flash('item already in cart')
            return redirect(url_for('main.order'))

    return render_template('order.html', order=order, totalprice=totalprice)


# Delete specific cart items (by clicking button to the right of item)
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))


# Delete ALL ITEMS in Cart
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))


# Checkout
@bp.route('/checkout/', methods=['POST', 'GET'])
def checkout():
    form = CheckoutForm()
    if 'order_id' in session:
        order = Order.query.get(session['order_id'])
        # if this fails (i.e. no order is retrieved), it automatically produces a 404 error

        if form.validate_on_submit():  # if form validated on pressing submit button
            order.status = True  # true = order is confirmed/checked out
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for product in order.products:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash(
                    'Thank you! Your order is confirmed. We will be sending a receipt to your email shortly!')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)
