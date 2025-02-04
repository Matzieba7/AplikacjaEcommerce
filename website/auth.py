from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, login_required, logout_user
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from .models import Customer
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Rejestracja nowego użytkownika.

    Returns:
        str: Renderowana strona HTML.
    """
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer(
                email=email,
                username=username,
                password=password2
            )

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Konto utworzone poprawnie! Możesz się teraz zalogować')
                return redirect('/login')
            except Exception as e:
                flash('Konto nie zostało utworzone! Adres email już istnieje')
                print(e)

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logowanie użytkownika.

    Returns:
        str: Renderowana strona HTML.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Niepoprawny email lub hasło')
        else:
            flash('Konto nie istnieje. Proszę się zarejestrować')

    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    """
    Wylogowanie użytkownika.

    Returns:
        Response: Przekierowanie na stronę główną.
    """
    logout_user()
    return redirect('/')

@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    """
    Wyświetlanie profilu użytkownika.

    Args:
        customer_id (int): ID użytkownika.

    Returns:
        str: Renderowana strona HTML.
    """
    customer = Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)

@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    """
    Zmiana hasła użytkownika.

    Args:
        customer_id (int): ID użytkownika.

    Returns:
        str: Renderowana strona HTML.
    """
    form = PasswordChangeForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Hasło zaktualizowane')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('Hasła się nie zgadzają!')
        else:
            flash('Obecne hasło jest niepoprawne')

    return render_template('change_password.html', form=form)
