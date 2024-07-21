from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Customer(db.Model, UserMixin):
    """
    Model reprezentujący klienta.

    Attributes:
        id (int): ID klienta.
        email (str): Email klienta.
        username (str): Nazwa użytkownika.
        password_hash (str): Hash hasła klienta.
        date_joined (datetime): Data dołączenia.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.now)

    cart_items = db.relationship('Cart', backref=db.backref('customer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('customer', lazy=True))

    @property
    def password(self):
        """Blokowanie bezpośredniego dostępu do hasła."""
        raise AttributeError('Hasło nie jest atrybutem do odczytu')

    @password.setter
    def password(self, password):
        """Hashowanie hasła przed zapisem."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Weryfikacja hasła klienta.

        Args:
            password (str): Hasło do weryfikacji.

        Returns:
            bool: Czy hasło jest poprawne.
        """
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'<Klient {self.id}>'

class Product(db.Model):
    """
    Model reprezentujący produkt.

    Attributes:
        id (int): ID produktu.
        product_name (str): Nazwa produktu.
        current_price (float): Obecna cena.
        previous_price (float): Poprzednia cena.
        in_stock (int): Ilość na stanie.
        product_picture (str): Ścieżka do zdjęcia produktu.
        flash_sale (bool): Czy produkt jest na wyprzedaży.
        date_added (datetime): Data dodania.
    """
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))

    def __str__(self):
        return f'<Produkt {self.product_name}>'

class Cart(db.Model):
    """
    Model reprezentujący koszyk.

    Attributes:
        id (int): ID koszyka.
        quantity (int): Ilość produktów.
        customer_link (int): ID klienta.
        product_link (int): ID produktu.
    """
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return f'<Koszyk {self.id}>'

class Order(db.Model):
    """
    Model reprezentujący zamówienie.

    Attributes:
        id (int): ID zamówienia.
        quantity (int): Ilość produktów.
        price (float): Cena zamówienia.
        status (str): Status zamówienia.
        payment_id (str): ID płatności.
        customer_link (int): ID klienta.
        product_link (int): ID produktu.
    """
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return f'<Zamówienie {self.id}>'
