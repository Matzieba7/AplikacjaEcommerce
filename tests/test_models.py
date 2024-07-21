def test_new_customer(new_customer):
    assert new_customer.email == 'test@test.com'
    assert new_customer.username == 'testuser'
    assert new_customer.password_hash != 'testpassword'  # Password should be hashed

def test_new_product(new_product):
    assert new_product.product_name == 'Test Product'
    assert new_product.current_price == 10.0
    assert new_product.previous_price == 15.0
    assert new_product.in_stock == 100