from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db, login_manager
from .forms import LoginForm, RegisterForm

import requests
import jwt

index_blueprint = Blueprint("index", __name__)
session_blueprint = Blueprint("session", __name__)
functionality_blueprint = Blueprint("functionality", __name__)
menu_blueprint = Blueprint("menu", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@index_blueprint.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("session.login"))


@session_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(form.username.data)
        print(user)
        if user:
            if check_password_hash(user.password, form.password.data):
                print('checked')
                login_user(user, remember=form.remember.data)
                return redirect(url_for("functionality.dashboard"))

        # return '<h1>Invalid username or password</h1>'
        flash("Invalid username or password", category="warning")

    return render_template("login.html", form=form)


@session_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        # flash("Your account has been successfully created.", category="success")
        return redirect(url_for("session.login"))

        # return '<h1>New user has been created!</h1>'

    return render_template("signup.html", form=form)


@session_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been successfully log out.", category="success")
    return redirect(url_for("index.index"))


@functionality_blueprint.route("/dashboard")
@login_required
def dashboard():
    jwt_token = jwt.encode({}, "haslo123", algorithm="HS256")
    try:
        resp = requests.get(
            "http://127.0.0.1:5000/all_assets",
            headers={"X-Access-Token": jwt_token},
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        return render_template(
            "dashboard.html", name=current_user.username, assets=[], is_error=True
        )

    if resp.status_code != 200:
        return render_template(
            "dashboard.html", name=current_user.username, assets=[], is_error=True
        )

    payload = resp.json()
    assets = []  # [{'name': 'Apple', 'abbr': 'A'}, {'}]
    for asset in payload:
        abbr = asset["abbreviation"]
        name = asset["name"]
        assets.append({"abbr": abbr, "name": name})

    return render_template(
        "dashboard.html", name=current_user.username, assets=assets, is_error=False
    )


@menu_blueprint.route("/portfolio")
@login_required
def portfolio():
    jwt_token = jwt.encode({}, "haslo123", algorithm="HS256")
    try:
        resp = requests.get(
            f"http://127.0.0.1:5000/assets/{current_user.username}",
            headers={"X-Access-Token": jwt_token},
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        assets = ["Currently not available"]
    else:
        if resp.status_code != 200:
            assets = ["Currently not available"]
        else:
            assets = resp.json()["available_assets"]
            print(resp.status_code)

    return render_template("portfolio.html", assets=assets)


@menu_blueprint.route("/account")
@login_required
def account():
    return render_template("account.html", name=current_user.username)
