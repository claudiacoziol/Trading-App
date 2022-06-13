import os

from flask_app import create_app, db
from flask_app.models import User

if __name__ == "__main__":
    app = create_app()

    if not os.path.exists("users_database.sqlite3"):
        with app.app_context():
            db.create_all()

    app.debug = True
    app.run(host="0.0.0.0", port=5001)
