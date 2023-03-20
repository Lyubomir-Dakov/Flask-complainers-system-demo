from marshmallow import fields, Schema
from marshmallow_enum import EnumField

from models import State
from schemas.bases import ComplainRequestBaseSchema


class ComplaintResponseSchema(ComplainRequestBaseSchema):
    id = fields.Integer(required=True)
    status = EnumField(State, by_value=True)
    created_on = fields.DateTime(required=True)
    complainer_id = fields.Integer(required=True)


#     TODO Nest user inside


class ComplaintsResponseSchema(Schema):
    complaints = fields.Nested(ComplaintResponseSchema, many=True)
