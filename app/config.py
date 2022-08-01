from decouple import config


class Config:
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@app_db:5432/users_db"
