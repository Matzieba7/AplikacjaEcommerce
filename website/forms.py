from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField

class SignUpForm(FlaskForm):
    """
    Formularz rejestracji użytkownika.
    """
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2)])
    password1 = PasswordField('Hasło', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Powtórz hasło', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Zarejestruj się')

class LoginForm(FlaskForm):
    """
    Formularz logowania użytkownika.
    """
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

class PasswordChangeForm(FlaskForm):
    """
    Formularz zmiany hasła użytkownika.
    """
    current_password = PasswordField('Obecne hasło', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('Nowe hasło', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Powtórz nowe hasło', validators=[DataRequired(), Length(min=6)])
    change_password = SubmitField('Zmień hasło')

class ShopItemsForm(FlaskForm):
    """
    Formularz dodawania i aktualizacji produktów.
    """
    product_name = StringField('Produkt', validators=[DataRequired()])
    current_price = FloatField('Obecna cena', validators=[DataRequired()])
    previous_price = FloatField('Stara cena', validators=[DataRequired()])
    in_stock = IntegerField('Na stanie', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Ikona', validators=[DataRequired()])
    flash_sale = BooleanField('Wyprzedaże')
    add_product = SubmitField('Dodaj')
    update_product = SubmitField('Zaktualizuj')

class OrderForm(FlaskForm):
    """
    Formularz aktualizacji statusu zamówienia.
    """
    order_status = SelectField('Status zamówienia',
                               choices=[('W trakcie', 'W trakcie'),
                                        ('Zaakceptowane', 'Zaakceptowane'),
                                        ('Wysłane', 'Wysłane'),
                                        ('Dostarczone', 'Dostarczone'),
                                        ('Anulowane', 'Anulowane')])
    update = SubmitField('Aktualizuj status')
