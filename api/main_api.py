import sqlalchemy
from flask import Blueprint, request, Response

from __init__ import db
from models import (
    Assets,
    AssetSchema,
    AssetPriceHistorySchema,
    AssetsUsers,
    AssetsPriceHistory,
)
from decorators import token_required

add_asset_blueprint = Blueprint("add_asset", __name__)
add_user_to_asset_blueprint = Blueprint("add_user_to_asset", __name__)
add_current_price_blueprint = Blueprint("add_current_price", __name__)
get_assets_by_username_blueprint = Blueprint("get_assets_by_username", __name__)
get_assets_blueprint = Blueprint("get_assets", __name__)
get_asset_blueprint = Blueprint("get_asset", __name__)
get_asset_history_blueprint = Blueprint("get_asset_history", __name__)
get_asset_current_value_blueprint = Blueprint("get_asset_current_value", __name__)
delete_asset_blueprint = Blueprint("delete_asset", __name__)

asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)
asset_price_history_schema = AssetPriceHistorySchema(many=True)


def add_to_db(new_asset: Assets) -> None:
    db.session.add(new_asset)
    db.session.commit()


def delete_from_db(asset_to_delete: Assets) -> None:
    db.session.delete(asset_to_delete)
    db.session.commit()


@get_assets_blueprint.route("/user_assets/<string:nickname>")
# @token_required
def get_assets_from_user(nickname: str) -> str:
    found_data = AssetsUsers.query.filter_by(username=nickname).all()
    assets = list(map(lambda row: row.asset_name, found_data))
    return assets


@add_asset_blueprint.route("/asset", methods=["POST"])
# @token_required
def add_asset() -> str:
    body = request.json
    new_asset = Assets.create_from_json(json_body=body)
    add_to_db(new_asset)

    return asset_schema.jsonify(new_asset)


@add_user_to_asset_blueprint.route("/user_to_asset", methods=["POST"])
# @token_required
def add_user_to_asset() -> Response:
    """
    expected JSON body:
    {
        'username': <username>,
        'asset_name': <username>
    }

    :return:
    """
    data = request.json
    username = data["username"]
    asset_name = data["asset_name"]
    new_pair = AssetsUsers(asset_name, username)
    try:
        add_to_db(new_pair)
    except sqlalchemy.exc.IntegrityError:
        return "Invalid Data", 500

    return "Success!", 201


@add_current_price_blueprint.route(
    "/asset/<string:abbr>", methods=["POST"]
)  
def add_current_price(abbr: str) -> Response:
    '''
    expected url format: /asset/abb?new_price=100&date=
    '''
    current_price = request.args["new_price"]
    found_asset_id = Assets.query.filter_by(abbreviation=abbr).first()._id
    new_history_price = AssetsPriceHistory(current_price, found_asset_id)

    add_to_db(new_history_price)

    return "History updated!", 201


@get_assets_by_username_blueprint.route("/assets/<string:username>")
# @token_required
def get_assets_by_username(username: str) -> Response:
    assets = AssetsUsers.query.filter_by(username=username).all()
    names = list(map(lambda row: row.asset_name, assets))
    return {"available_assets": names, "name": username}


@get_assets_blueprint.route("/all_assets")
# @token_required
def get_assets() -> Response:
    all_assets = Assets.query.all()

    return assets_schema.jsonify(all_assets)


@get_asset_blueprint.route("/asset/<int:id>")
# @token_required
def get_asset_by_id(id: int) -> Response:
    found_asset = Assets.query.get(id)

    return asset_schema.jsonify(found_asset)


@get_asset_history_blueprint.route("/history/<string:abbr>")
# @token_required
def asset_history(abbr:str) -> Response:
    found_asset_id = Assets.query.filter_by(abbreviation=abbr).first()._id
    history_records = AssetsPriceHistory.query.filter_by(asset_id=found_asset_id).all()

    return asset_price_history_schema.jsonify(history_records)


@get_asset_current_value_blueprint.route("/asset/<string:abbr>/value")
# @token_required
def asset_current_value(abbr:str) -> Response:
    def jsonify_data():
        while True:
            found_asset_id = Assets.query.filter_by(abbreviation=abbr).first()._id
            current_value = AssetsPriceHistory.query.filter_by(
                asset_id=found_asset_id
            ).first()
            yield current_value

    return {"current_value": jsonify_data()}


@delete_asset_blueprint.route("/asset/<int:id>", methods=["DELETE"])
# @token_required
def delete_asset(id: int) -> Response:
    asset_to_delete = Assets.query.get(id)
    delete_from_db(asset_to_delete)

    return asset_schema.jsonify(asset_to_delete)

