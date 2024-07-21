from flask import Blueprint, render_template, flash, redirect, request
from .models import Product
from flask_login import login_required, current_user
from .models import Cart
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():

    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
    if current_user.is_authenticated else [])

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f' Ilość produktu: { item_exists.product.product_name } została zaktualizowana')
            return redirect(request.referrer)
        except Exception as e:
            print('Ilość produktu nie została zaktualizowana', e)
            flash(f'Ilość produktu: { item_exists.product.product_name } nie została zaktualizowana')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'Produkt: {new_cart_item.product.product_name} został dodany do koszyka')
    except Exception as e:
        print('Produkt nie został dodany do koszyka', e)
        flash(f'Produkt: {new_cart_item.product.product_name} nie został dodany do koszyka')

    return redirect(request.referrer)

@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount+200)