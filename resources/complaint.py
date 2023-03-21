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


class ComplaintResource(Resource):
    def post(self, pk):
        pass

    def get(self, pk):
        pass

    # TODO For homework -
    #  we have to create manager who deletes the complaint and it should return 204
    #  (have to use BadRequest from marshmallow)
    @auth.login_required()
    @permission_required(RoleType.admin)
    def delete(self,pk):
        ComplaintManager.delete_complaint(pk)


class ComplaintApproveResource(Resource):
    @auth.login_required()
    @permission_required(RoleType.approver)
    def get(self, pk):
        ComplaintManager.approve_complaint(pk)


class ComplaintRejectResource(Resource):
    @auth.login_required()
    @permission_required(RoleType.approver)
    def get(self, pk):
        ComplaintManager.reject_complaint(pk)
