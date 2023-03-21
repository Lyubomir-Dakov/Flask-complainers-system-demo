from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth
from models import ComplaintModel


def validate_schema(schema_name):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(errors)
            return func(*args, **kwargs)

        return wrapper

    return decorated_func


def permission_required(permission_role):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role == permission_role:
                return func(*args, **kwargs)
            raise Forbidden("You do not have permission to access this resources")

        return wrapper

    return decorated_func
