import requests
from flask import request
from flask_login import current_user


def add_new_asset():
    chosen_asset = str(request.form["asset_choice"])
    requests.post(
        "http://api:5001/user_to_asset",
        json={"username": current_user.username, "asset_name": chosen_asset},
    )
    flash("New asset's been added to your portfolio succesfully.")
    return redirect(url_for("menu.portfolio"))


def prepare_assets(resp: requests.Response):
    payload = resp.json()
    assets = []
    for asset in payload:
        abbr = asset["abbreviation"]
        name = asset["name"]
        assets.append({"abbr": abbr, "name": name})
    return assets