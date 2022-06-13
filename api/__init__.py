from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import Config
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    migrate.init_app(app, db)
    db.init_app(app)
    ma.init_app(app)

    from .main_api import (
        add_asset_blueprint,
        add_user_to_asset_blueprint,
        add_current_price_blueprint,
        get_assets_by_username_blueprint,
        get_assets_blueprint,
        get_asset_blueprint,
        get_asset_history_blueprint,
        delete_asset_blueprint,
    )

    app.register_blueprint(add_asset_blueprint)
    app.register_blueprint(add_user_to_asset_blueprint)
    app.register_blueprint(add_current_price_blueprint)
    app.register_blueprint(get_assets_by_username_blueprint)
    app.register_blueprint(get_assets_blueprint)
    app.register_blueprint(get_asset_blueprint)
    app.register_blueprint(get_asset_history_blueprint)
    app.register_blueprint(delete_asset_blueprint)

    return app
