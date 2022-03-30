from __future__ import annotations
from __init__ import db, ma
from flask_marshmallow import fields


class Assets(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(length=5), nullable=False)

    def __init__(self, name: str, abbreviation: str):
        self.name = name
        self.abbreviation = abbreviation

    @staticmethod
    def create_from_json(json_body: dict) -> Assets:

        return Assets(name=json_body["name"], abbreviation=json_body["abbreviation"])


class AssetsUsers(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(length=50), db.ForeignKey("Assets.name"))
    username = db.Column(db.String(length=15), nullable=False, unique=True)


class AssetSchema(ma.Schema):
    _id = fields.fields.Integer()
    name = fields.fields.Str()
    abbreviation = fields.fields.Str()
