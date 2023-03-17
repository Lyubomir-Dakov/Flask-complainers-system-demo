from flask_restful import Resource

from managers.auth import auth
from managers.complain import ComplaintManager
from schemas.request.complaint import RequestComplainSchema
from schemas.response.complaint import ComplaintResponseSchema
from utils.decorators import validate_schema


class ComplaintListCreateResource(Resource):
    @auth.login_required
    @validate_schema(RequestComplainSchema)
    def get(self):
        user = auth.current_user()
        complains = ComplaintManager.get_all_complainer_claims(user)
        return ComplaintResponseSchema().dump(complains, many=True)

    def post(self):
        pass
