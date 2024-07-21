from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired

class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Hasło', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Powtórz hasło', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Zarejestruj się')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Obecne hasło', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('Nowe hasło', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Powtórz nowe hasło', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Zmień hasło')

class ShopItemsForm(FlaskForm):
    product_name = StringField('Produkt', validators=[DataRequired()])
    current_price = FloatField('Obecna cena', validators=[DataRequired()])
    previous_price = FloatField('Stara cenaP', validators=[DataRequired()])
    in_stock = IntegerField('Na stanie', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Ikona', validators=[DataRequired()])
    flash_sale = BooleanField('Wyprzedaże')

    add_product = SubmitField('Dodaj')
    update_product = SubmitField('Zaktualizuj')

class OrderForm(FlaskForm):
    order_status = SelectField('Status zamówienia', choices=[('W trakcie', 'W trakcie'), ('Zaakceptowane', 'Zaakceptowane'),
                                                        ('Wysłane', 'Wysłane'),
                                                        ('Dostarczone', 'Dostarczone'), ('Anulowane', 'Anulowane')])

    update = SubmitField('Aktualizuj status')