"""Update tbl_books schema

Revision ID: ac118cd2cdda
Revises: dafdfd716cc2
Create Date: 2021-05-07 20:45:51.106994

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'ac118cd2cdda'
down_revision = 'dafdfd716cc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_tbl_books_isbn', 'tbl_books', ['isbn'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_tbl_books_isbn', 'tbl_books', type_='unique')
    # ### end Alembic commands ###
