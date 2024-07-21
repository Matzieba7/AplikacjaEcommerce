from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import ShopItemsForm, OrderForm
from .models import Product, Order, Customer
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    """
    Wysyła plik graficzny z katalogu 'media'.

    Args:
        filename (str): Nazwa pliku do wysłania.

    Returns:
        Response: Plik graficzny.
    """
    return send_from_directory('../media', filename)

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    """
    Dodaje nowe przedmioty do sklepu. Dostępne tylko dla administratora.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        form = ShopItemsForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_shop_item = Product(
                product_name=product_name,
                current_price=current_price,
                previous_price=previous_price,
                in_stock=in_stock,
                flash_sale=flash_sale,
                product_picture=file_path
            )

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'Produkt {product_name} dodany poprawnie')
                return render_template('add_shop_items.html', form=form)
            except Exception as e:
                flash('Produkt nie został poprawnie dodany!')
                print(e)

        return render_template('add_shop_items.html', form=form)

    return render_template('404.html')

@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    """
    Wyświetla przedmioty w sklepie. Dostępne tylko dla administratora.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')

@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    """
    Aktualizuje informacje o przedmiocie w sklepie. Dostępne tylko dla administratora.

    Args:
        item_id (int): ID przedmiotu do aktualizacji.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        form = ShopItemsForm()
        item_to_update = Product.query.get(item_id)

        form.product_name.data = item_to_update.product_name
        form.previous_price.data = item_to_update.previous_price
        form.current_price.data = item_to_update.current_price
        form.in_stock.data = item_to_update.in_stock
        form.flash_sale.data = item_to_update.flash_sale

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            if file:
                file_name = secure_filename(file.filename)
                file_path = f'./media/{file_name}'
                file.save(file_path)
            else:
                file_path = item_to_update.product_picture

            try:
                Product.query.filter_by(id=item_id).update({
                    'product_name': product_name,
                    'current_price': current_price,
                    'previous_price': previous_price,
                    'in_stock': in_stock,
                    'flash_sale': flash_sale,
                    'product_picture': file_path
                })
                db.session.commit()
                flash(f'Produkt {product_name} zaktualizowany pomyślnie')
                return redirect('/shop-items')
            except Exception as e:
                flash('Produkt nie został zaktualizowany!')
                print(e)

        return render_template('update_item.html', form=form)
    return render_template('404.html')

@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    """
    Usuwa przedmiot ze sklepu. Dostępne tylko dla administratora.

    Args:
        item_id (int): ID przedmiotu do usunięcia.

    Returns:
        str: Przekierowanie na stronę z przedmiotami w sklepie.
    """
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Produkt usunięty')
        except Exception as e:
            flash('Produkt nie został usunięty!')
            print('Produkt nie został usunięty. Błąd:', e)
        return redirect('/shop-items')

    return render_template('404.html')

@admin.route('/view-orders')
@login_required
def order_view():
    """
    Wyświetla zamówienia. Dostępne tylko dla administratora.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')

@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    """
    Aktualizuje status zamówienia. Dostępne tylko dla administratora.

    Args:
        order_id (int): ID zamówienia do aktualizacji.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        form = OrderForm()
        order = Order.query.get(order_id)

        if form.validate_on_submit():
            order.status = form.order_status.data

            try:
                db.session.commit()
                flash(f'Zamówienie {order_id} zaktualizowano pomyślnie')
                return redirect('/view-orders')
            except Exception as e:
                flash(f'Zamówienie {order_id} nie zostało zaktualizowane')
                print(e)

        return render_template('order_update.html', form=form)

    return render_template('404.html')

@admin.route('/customers')
@login_required
def display_customers():
    """
    Wyświetla klientów. Dostępne tylko dla administratora.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')

@admin.route('/admin-page')
@login_required
def admin_page():
    """
    Wyświetla stronę administracyjną. Dostępne tylko dla administratora.

    Returns:
        str: Renderowana strona HTML.
    """
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')
