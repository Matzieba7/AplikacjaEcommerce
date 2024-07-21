import pytest
from website import create_app, db
from website.models import Product, Customer, Cart


@pytest.fixture(scope='module')
def new_customer():
    return Customer(email='test@test.com', username='testuser', password='testpassword')


@pytest.fixture(scope='module')
def new_product():
    return Product(product_name='Test Product', current_price=10.0, previous_price=15.0, in_stock=100,
                   product_picture='test.jpg')


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
    })

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert 'home' in response.get_data(as_text=True).lower()

