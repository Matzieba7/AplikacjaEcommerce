from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, NumberRange

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