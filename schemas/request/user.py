from marshmallow import fields

from schemas.bases import UserRequestBaseSchema


class RequestRegisterUserSchema(UserRequestBaseSchema):
    first_name = fields.String(min_length=2, max_length=20, required=True)
    last_name = fields.String(min_length=2, max_length=20, required=True)
    phone = fields.String(min_length=10, max_length=13, required=True)
    iban = fields.String(min_length=22, max_length=22, required=True)


class RequestLoginUserSchema(UserRequestBaseSchema):
    pass
