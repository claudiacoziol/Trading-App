from __future__ import annotations
from flask_marshmallow import fields
import datetime

from __init__ import db, ma

'''
AssetsHistory
asset_id (FK) timestamp curr_price
'''


class AssetsPriceHistory(db.Model):
    __tablename__ = "AssetsPriceHistory"
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    current_price = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    asset_id = db.Column(db.Integer, db.ForeignKey("Assets._id"))

    def __init__(self, current_price, asset, date=None):
        self.current_price = current_price
        self.date = date
        self.asset_id = asset


class Assets(db.Model):
    __tablename__ = "Assets"
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(length=5), nullable=False)
    prices = db.relationship("AssetsPriceHistory")

    def __init__(self, name: str, abbreviation: str):
        self.name = name
        self.abbreviation = abbreviation

    @staticmethod
    def create_from_json(json_body: dict) -> Assets:
        return Assets(name=json_body["name"], abbreviation=json_body["abbreviation"])


class AssetsUsers(db.Model):
    __tablename__ = "AssetsUsers"
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(length=50), db.ForeignKey("Assets.name"))
    username = db.Column(db.String(length=15), nullable=False)

    def __init__(self, asset_name: str, username: str):
        self.asset_name = asset_name
        self.username = username


class AssetSchema(ma.Schema):
    _id = fields.fields.Integer()
    name = fields.fields.Str()
    abbreviation = fields.fields.Str()


class AssetPriceHistorySchema(ma.Schema):
    _id = fields.fields.Integer()
    current_price = fields.fields.Float()
    date = fields.fields.DateTime()
    asset_id = fields.fields.Integer()