from alice_app.dependency_injection import configure_inject
configure_inject()

from flask import Flask
from alice_app.views.oauth import mod as oauth
from alice_app.views.smart_home import mod as smart_home

PREFIX = '/alicehm'


def create_app():
    app = Flask(__name__)

    app.register_blueprint(oauth, url_prefix=f'{PREFIX}/oauth')
    app.register_blueprint(smart_home, url_prefix=f'{PREFIX}/v1.0')
    return app
