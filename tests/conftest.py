import pytest
from website import create_app
from website.models import db, Customer, Product

@pytest.fixture(scope='module')
def new_customer():
    customer = Customer(email='test@test.com', username='testuser', password='testpassword')
    return customer

@pytest.fixture(scope='module')
def new_product():
    product = Product(product_name='Test Product', current_price=10.0, previous_price=15.0, in_stock=100, product_picture='path/to/picture.jpg')
    return product

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Configuring the app for testing
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()