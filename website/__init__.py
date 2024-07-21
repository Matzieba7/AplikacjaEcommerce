from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'

def create_database(app):
    """Tworzy bazę danych, jeśli nie istnieje i dodaje domyślne dane."""
    with app.app_context():
        db.create_all()
        print('Baza danych utworzona')
        create_default_admin()  # Dodaj domyślnego admina
def create_default_admin():
    """Tworzy domyślnego użytkownika admina, jeśli nie istnieje."""
    from .models import Customer  # Importuj model Customer

    # Sprawdź, czy użytkownik admin już istnieje
    admin_user = Customer.query.filter_by(email='admin@gmail.com').first()

    if not admin_user:
        # Utwórz nowego użytkownika admina
        admin_user = Customer(
            email='admin@gmail.com',
            username='admin',
            password=generate_password_hash('Admin1234')
        )
        db.session.add(admin_user)
        db.session.commit()
        print('Domyślny użytkownik admina został utworzony')

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'poqwe qwcelqwkcelwqkmc qwek'

    # Ścieżka do pliku bazy danych w katalogu 'instance'
    db_path = os.path.join(app.instance_path, DB_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Tworzenie bazy danych, jeśli nie istnieje
    if not os.path.exists(db_path):
        create_database(app)

    return app

# Funkcja sprawdzająca uprawnienia do zapisu
def ensure_db_writable(db_path):
    """Sprawdza, czy plik bazy danych ma uprawnienia do zapisu."""
    try:
        if not os.path.exists(db_path):
            open(db_path, 'w').close()  # Tworzy plik, jeśli nie istnieje
        with open(db_path, 'a'):
            os.utime(db_path, None)
    except IOError:
        print(f"Plik bazy danych {db_path} nie ma uprawnień do zapisu.")
        raise

# Sprawdź uprawnienia przed uruchomieniem aplikacji
app = create_app()
db_path = os.path.join(app.instance_path, DB_NAME)
ensure_db_writable(db_path)


