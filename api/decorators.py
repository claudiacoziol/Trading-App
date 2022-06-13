import jwt

from flask import request


def token_required(func):
    def inner():
        token = request.headers.get("X-Access-Token")

        if token is None:
            return "Missing X-Access-Token in request", 401

        try:
            jwt.decode(token, "haslo123", algoritms=["HS256"])
        except jwt.ExpiredSignatureError:
            return "Session expired", 419
        except jwt.InvalidTokenError:
            return "Invalid Token Error!", 401
        else:
            return func()

    return inner