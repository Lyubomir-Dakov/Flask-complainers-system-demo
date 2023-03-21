from werkzeug.exceptions import BadRequest

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

    @staticmethod
    def approve_complaint(complaint_id):
        ComplaintManager._validate_status(complaint_id)
        ComplaintModel.query.filter_by(id=complaint_id).update({"status": State.approved})
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintManager._validate_status(complaint_id)
        ComplaintModel.query.filter_by(id=complaint_id).update({"status": State.rejected})
        db.session.commit()

    @staticmethod
    def _validate_status(complaint_id):
        complaint = ComplaintModel.query.filter_by(id=complaint_id).first()
        if not complaint:
            raise BadRequest(f"Complaint with id {complaint_id} does not exists!")
        if not complaint.status == "pending":
            raise BadRequest("You are not allowed to change the status of already processed complaints")

role_mapper = {
    RoleType.complainer: ComplaintManager._get_complainer_complaint,
    RoleType.approver: ComplaintManager._get_approver_complaints,
    RoleType.admin: ComplaintManager._get_admin_complaints
}