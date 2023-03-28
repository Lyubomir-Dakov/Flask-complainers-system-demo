import uuid

from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from models import ComplaintModel, RoleType, State, TransactionModel
from services.wise import WiseService


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
        current_user = auth.current_user()
        full_name = f"{current_user.first_name} {current_user.last_name}"
        amount = data["amount"]
        data["complainer_id"] = complainer_id
        complaint = ComplaintModel(**data)
        iban = current_user.iban

        db.session.add(complaint)
        db.session.flush()

        transaction = ComplaintManager.issue_transfer(amount, iban, full_name, complaint.id)

        db.session.add(transaction)
        db.session.flush()
        return complaint

    @staticmethod
    def approve_complaint(complaint_id):
        ComplaintManager._validate_complaint_existence(complaint_id)
        ComplaintManager._validate_status(complaint_id)
        ComplaintModel.query.filter_by(id=complaint_id).update({"status": State.approved})
        service = WiseService()
        transfer = TransactionModel.query.filter_by(complaint_id=complaint_id).first()
        service.fund_transfer(transfer_id=transfer.transfer_id)
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintManager._validate_complaint_existence(complaint_id)
        ComplaintManager._validate_status(complaint_id)
        ComplaintModel.query.filter_by(id=complaint_id).update({"status": State.rejected})
        service = WiseService()
        transfer = TransactionModel.query.filter_by(complaint_id=complaint_id).first()
        service.cancel_transfer(transfer.transfer_id)
        db.session.commit()

    @staticmethod
    def _validate_status(complaint_id):
        complaint = ComplaintModel.query.filter_by(id=complaint_id).first()
        if not complaint.status.value == "pending":
            raise BadRequest("You are not allowed to change the status of already processed complaints")

    @staticmethod
    def _validate_complaint_existence(complaint_id):
        complaint = ComplaintModel.query.filter_by(id=complaint_id).first()
        if not complaint:
            raise BadRequest(f"Complaint with id {complaint_id} does not exists!")

    @staticmethod
    def delete_complaint(complaint_id):
        ComplaintManager._validate_complaint_existence(complaint_id)
        complaint = ComplaintModel.query.filter_by(id=complaint_id).first()
        db.session.delete(complaint)
        db.session.commit()
        return "", 204

    @staticmethod
    def issue_transfer(amount, iban, full_name, complaint_id):
        service = WiseService()
        quote_id = service.create_quote(amount)

        recipient_id = service.create_recipient(full_name, iban)
        custom_transaction_id = str(uuid.uuid4())
        transfer_id = service.create_transfer(recipient_account_id=recipient_id, quote_id=quote_id,
                                              custom_transaction_id=custom_transaction_id)
        transaction = TransactionModel(
            quote_id=quote_id,
            transfer_id=transfer_id,
            custom_transfer_id=custom_transaction_id,
            target_account_id=recipient_id,
            amount=amount,
            complaint_id=complaint_id
        )
        return transaction


role_mapper = {
    RoleType.complainer: ComplaintManager._get_complainer_complaint,
    RoleType.approver: ComplaintManager._get_approver_complaints,
    RoleType.admin: ComplaintManager._get_admin_complaints
}
