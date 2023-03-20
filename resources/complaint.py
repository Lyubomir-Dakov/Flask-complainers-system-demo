from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complain import ComplaintManager
from models import RoleType
from schemas.request.complaint import RequestComplainSchema
from schemas.response.complaint import ComplaintResponseSchema
from utils.decorators import validate_schema, permission_required


class ComplaintListCreateResource(Resource):
    @auth.login_required
    # @validate_schema(RequestComplainSchema)
    def get(self):
        # current_user = auth.current_user()
        complaints = ComplaintManager.get_complaints()
        return ComplaintResponseSchema().dump(complaints, many=True)


    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(RequestComplainSchema)
    def post(self):
        complainer = auth.current_user()
        data = request.get_json()
        complain = ComplaintManager.create(data, complainer.id)
        # Use dump, not load when schema and object are not the same
        return ComplaintResponseSchema().dump(complain)
