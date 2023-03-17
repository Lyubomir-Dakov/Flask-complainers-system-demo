from db import db
from models import ComplaintModel, ComplainerModel


class ComplaintManager:
    @staticmethod
    def get_all_complainer_claims(user):
        if isinstance(user, ComplainerModel):
            return ComplaintModel.query.filter_by(complainer_id=user.id).all()
        return ComplaintModel.query.all()

    @staticmethod
    def create(data, complainer_id):
        data["complainer_id"] = complainer_id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.flush()
        return complaint
