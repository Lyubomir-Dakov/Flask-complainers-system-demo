from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import DecodeError
from werkzeug.exceptions import Unauthorized, BadRequest

from models import ComplainerModel


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
        except DecodeError as ex:
            raise BadRequest("Invalid or missing token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        user = ComplainerModel.query.filter_by(id=user_id).first()
        # return eval(f"{type_user}.query.filter_by(id={user_id}).first()")
        if not user:
            raise Unauthorized("Invalid or missing token")
        return user
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
