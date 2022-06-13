from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import timedelta
from config import Config

db = SQLAlchemy()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    encryptor = md5()

    login_manager.init_app(app)
    login_manager.login_view = "login"

    app.permanent_session_lifetime = timedelta(minutes=60)
    app.secret_key = encryptor.digest()

    db.init_app(app)

    from .views import (
        index_blueprint,
        session_blueprint,
        functionality_blueprint,
        menu_blueprint,
    )

    app.register_blueprint(index_blueprint)
    app.register_blueprint(session_blueprint)
    app.register_blueprint(functionality_blueprint)
    app.register_blueprint(menu_blueprint)

    app.debug = True

    return app
