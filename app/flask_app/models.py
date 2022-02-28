from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        self.username, self.email, self.password = username, email, hashed_password


# db.create_all()
# db.session.commit()

