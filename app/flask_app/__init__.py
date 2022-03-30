from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import timedelta
from decouple import config

db = SQLAlchemy()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    encryptor = md5()
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    app.permanent_session_lifetime = timedelta(minutes=60)
    app.secret_key = encryptor.digest()
    app.config["SECRET_KEY"] = config("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users_database.sqlite3"
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
