from flask import Blueprint, render_template, flash, redirect, request, jsonify
from .models import Product
from flask_login import login_required, current_user
from .models import Cart, Order
from . import db
from flask import make_response
import xml.etree.ElementTree as ET

views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_ca0331cb-8a01-4510-a711-e2260071ccb8'

API_TOKEN = 'ISSecretKey_test_c6f63b6f-06f6-441d-b5f0-dec432e2a0bd'

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

@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)


@views.route('/removecart', methods=['POST'])
@login_required
def remove_cart():
    cart_id = request.form.get('cart_id')
    cart_item = Cart.query.get(cart_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        data = {
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)
    return jsonify({'error': 'Item not found'}), 404

@views.route('/place-order', methods=['POST'])
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if customer_cart:
        try:
            total = sum(item.product.current_price * item.quantity for item in customer_cart)

            order_status = "W trakcie"

            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price
                new_order.status = order_status
                new_order.payment_id = ""

                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link

                db.session.add(new_order)

                product = Product.query.get(item.product_link)
                product.in_stock -= item.quantity

                db.session.delete(item)

            db.session.commit()

            flash('Zamówienie złożone poprawnie')
            return redirect('/orders')
        except Exception as e:
            print(e)
            flash('Zamówienie nie zostało złożone')
            return redirect('/')
    else:
        flash('Twój koszyk jest pusty')
        return redirect('/')

@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)


@views.route('/export-orders')
@login_required
def export_orders():
    orders = Order.query.filter_by(customer_link=current_user.id).all()

    root = ET.Element("Orders")

    for order in orders:
        order_elem = ET.SubElement(root, "Order")
        product_name = ET.SubElement(order_elem, "ProductName")
        product_name.text = order.product.product_name
        quantity = ET.SubElement(order_elem, "Quantity")
        quantity.text = str(order.quantity)
        price = ET.SubElement(order_elem, "Price")
        price.text = str(order.price)
        status = ET.SubElement(order_elem, "Status")
        status.text = order.status

    tree = ET.ElementTree(root)
    xml_data = ET.tostring(root, encoding='utf-8', method='xml')

    response = make_response(xml_data)
    response.headers['Content-Type'] = 'application/xml'
    response.headers['Content-Disposition'] = 'attachment; filename=orders.xml'

    return response
