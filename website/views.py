from flask import Blueprint, render_template, flash, redirect, request, jsonify, make_response
from .models import Product, Cart, Order
from flask_login import login_required, current_user
from . import db
import xml.etree.ElementTree as ET

views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_ca0331cb-8a01-4510-a711-e2260071ccb8'
API_TOKEN = 'ISSecretKey_test_c6f63b6f-06f6-441d-b5f0-dec432e2a0bd'

@views.route('/')
def home():
    """
    Widok głównej strony aplikacji.

    Returns:
        Renderowanie szablonu głównej strony z produktami na wyprzedaży oraz koszykiem użytkownika.
    """
    items = Product.query.filter_by(flash_sale=True)
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else []
    return render_template('home.html', items=items, cart=cart_items)

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    """
    Dodanie produktu do koszyka.

    Args:
        item_id (int): ID produktu do dodania.

    Returns:
        Przekierowanie do poprzedniej strony.
    """
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()

    if item_exists:
        try:
            item_exists.quantity += 1
            db.session.commit()
            flash(f'Ilość produktu: {item_exists.product.product_name} została zaktualizowana')
        except Exception as e:
            print('Ilość produktu nie została zaktualizowana', e)
            flash(f'Ilość produktu: {item_exists.product.product_name} nie została zaktualizowana')
        return redirect(request.referrer)

    new_cart_item = Cart(
        quantity=1,
        product_link=item_to_add.id,
        customer_link=current_user.id
    )

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
    """
    Wyświetlanie koszyka użytkownika.

    Returns:
        Renderowanie szablonu koszyka.
    """
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    return render_template('cart.html', cart=cart, amount=amount, total=amount + 200)

@views.route('/pluscart')
@login_required
def plus_cart():
    """
    Zwiększenie ilości produktu w koszyku.

    Returns:
        json: Zaktualizowane dane koszyka.
    """
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity += 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)

@views.route('/minuscart')
@login_required
def minus_cart():
    """
    Zmniejszenie ilości produktu w koszyku.

    Returns:
        json: Zaktualizowane dane koszyka.
    """
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity -= 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)

@views.route('/removecart', methods=['POST'])
@login_required
def remove_cart():
    """
    Usunięcie produktu z koszyka.

    Returns:
        json: Zaktualizowane dane koszyka lub błąd.
    """
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
    """
    Złożenie zamówienia.

    Returns:
        Przekierowanie do strony zamówień lub głównej z odpowiednim komunikatem.
    """
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if customer_cart:
        try:
            total = sum(item.product.current_price * item.quantity for item in customer_cart)
            order_status = "W trakcie"

            for item in customer_cart:
                new_order = Order(
                    quantity=item.quantity,
                    price=item.product.current_price,
                    status=order_status,
                    payment_id="",
                    product_link=item.product_link,
                    customer_link=item.customer_link
                )
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
    """
    Wyświetlanie zamówień użytkownika.

    Returns:
        Renderowanie szablonu zamówień.
    """
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)

@views.route('/export-orders')
@login_required
def export_orders():
    """
    Eksportowanie zamówień użytkownika do pliku XML.

    Returns:
        response: Plik XML z zamówieniami użytkownika.
    """
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
