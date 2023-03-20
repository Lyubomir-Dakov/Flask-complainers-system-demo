from db import db
from managers.auth import auth
from models import ComplaintModel, ComplainerModel, RoleType, State


class ComplaintManager:
    # @staticmethod
    # def get_all_complainer_claims(user):
    #     if isinstance(user, ComplainerModel):
    #         return ComplaintModel.query.filter_by(complainer_id=user.id).all()
    #     return ComplaintModel.query.all()
    @staticmethod
    def get_complaints():
        current_user = auth.current_user()
        role = current_user.role
        complaints = role_mapper[role]()
        return complaints

    @staticmethod
    def _get_complainer_complaint():
        current_user = auth.current_user()
        return ComplaintModel.query.filter_by(complainer_id=current_user.id).all()

    @staticmethod
    def _get_approver_complaints():
        return ComplaintModel.query.filter_by(State.pending).all()

    @staticmethod
    def _get_admin_complaints():
        return ComplaintModel.query.all()

    @staticmethod
    def create(data, complainer_id):
        data["complainer_id"] = complainer_id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.flush()
        return complaint


role_mapper = {
    RoleType.complainer: ComplaintManager._get_complainer_complaint,
    RoleType.approver: ComplaintManager._get_approver_complaints,
    RoleType.admin: ComplaintManager._get_admin_complaints
}