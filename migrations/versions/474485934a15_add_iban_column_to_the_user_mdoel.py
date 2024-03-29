"""add iban column to the user mdoel

Revision ID: 474485934a15
Revises: 5c6b24676d8a
Create Date: 2023-03-17 05:38:19.495174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '474485934a15'
down_revision = '5c6b24676d8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('iban', sa.String(length=22), nullable=True))
    op.add_column('approvers', sa.Column('iban', sa.String(length=22), nullable=True))
    op.add_column('complainers', sa.Column('iban', sa.String(length=22), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('complainers', 'iban')
    op.drop_column('approvers', 'iban')
    op.drop_column('admins', 'iban')
    # ### end Alembic commands ###
