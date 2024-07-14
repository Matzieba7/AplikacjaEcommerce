from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Ekran logowania aplikacji ecommerce'

@auth.route('/sign-up')
def sign_up():
    return 'Ekran rejestracji aplikacji ecommerce'