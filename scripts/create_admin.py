from werkzeug.security import generate_password_hash

from db import db
from models import AdministratorModel, RoleType


def create_admin(first_name, last_name, email, phone, password, iban):
    password = generate_password_hash(password, )
    admin = AdministratorModel(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        password=password,
        iban=iban,
        role=RoleType.admin
    )
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    # TODO Add values to be fetched from terminal
    create_admin()
