from flask import Blueprint, request, jsonify
from __init__ import db
from models import Assets, AssetSchema

import jwt
from decouple import config

add_asset_blueprint = Blueprint("add_asset", __name__)
get_assets_blueprint = Blueprint("get_assets", __name__)
get_asset_blueprint = Blueprint("get_asset", __name__)
delete_asset_blueprint = Blueprint("delete_asset", __name__)

asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)


def add_to_db(new_asset: Assets) -> None:
    db.session.add(new_asset)
    db.session.commit()


def delete_from_db(asset_to_delete: Assets) -> None:
    db.session.delete(asset_to_delete)
    db.session.commit()


@get_assets_blueprint.route('/user_assets/<string:nickname>')
def get_assets_from_user(nickname):
    # get from model AssetsUsers only those records which have chosen nickname
    found_data = AssetsUsers.query.filter_by(username=nickname).all()
    for row in found_data:
        asset = row.asset_name


@add_asset_blueprint.route("/asset", methods=["POST"])
def add_asset() -> str:
    body = request.json

    new_asset = Assets.create_from_json(json_body=body)

    add_to_db(new_asset)

    return asset_schema.jsonify(new_asset)


@get_assets_blueprint.route("/all_assets", methods=["GET"])
def get_assets():
    # extract token and check its validity
    token = request.headers.get("X-Access-Token")
    print(type(token))
    try:
        jwt.decode(token.strip(), "haslo123", algoritms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "Session expired", 419
    except jwt.InvalidTokenError:
        return "Invalid Token Error!", 401

    all_assets = Assets.query.all()
    return assets_schema.jsonify(all_assets)


@get_asset_blueprint.route("/asset/<int:id>", methods=["GET"])
def get_asset_by_id(id: int) -> str:
    found_asset = Assets.query.get(id)
    return asset_schema.jsonify(found_asset)


@delete_asset_blueprint.route("/asset/<int:id>", methods=["DELETE"])
def delete_asset(id: int) -> str:
    asset_to_delete = Assets.query.get(id)
    delete_from_db(asset_to_delete)

    return asset_schema.jsonify(asset_to_delete)
