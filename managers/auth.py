from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=2),
            "type": user.__class__.__name__}
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"])
            return info["sub"], info["type"]
        except Exception as ex:
            raise ex


auth = HTTPTokenAuth = HTTPTokenAuth

# @auth.verify_token
# def verify_token(token):
#     pass

