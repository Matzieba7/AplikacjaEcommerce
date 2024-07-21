import pytest
from website import create_app
from website.forms import SignUpForm

@pytest.fixture(scope='module')
def flask_app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    return app

@pytest.fixture(scope='module')
def client(flask_app):
    return flask_app.test_client()

@pytest.fixture(scope='module')
def app_context(flask_app):
    with flask_app.app_context():
        yield

def test_signup_form_valid(client, app_context):
    form = SignUpForm(email='newuser@test.com', username='newuser', password1='password', password2='password')
    assert form.validate()
