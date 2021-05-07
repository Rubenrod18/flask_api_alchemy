"""Add constraints to tbl_currencies

Revision ID: d7cfc86c6e35
Revises: ccff1682143e
Create Date: 2021-05-04 19:55:46.287705

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd7cfc86c6e35'
down_revision = 'ccff1682143e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        'uq_tbl_currencies_code', 'tbl_currencies', ['code']
    )
    op.create_unique_constraint(
        'uq_tbl_currencies_name', 'tbl_currencies', ['name']
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        'uq_tbl_currencies_name', 'tbl_currencies', type_='unique'
    )
    op.drop_constraint(
        'uq_tbl_currencies_code', 'tbl_currencies', type_='unique'
    )
    # ### end Alembic commands ###