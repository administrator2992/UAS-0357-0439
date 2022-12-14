"""empty message

Revision ID: 47a9677f5846
Revises: dda6165ea0bb
Create Date: 2022-07-30 07:14:40.683708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47a9677f5846'
down_revision = 'dda6165ea0bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'news', 'users', ['updated_by'], ['users_id'])
    op.create_foreign_key(None, 'news', 'users', ['created_by'], ['users_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'news', type_='foreignkey')
    op.drop_constraint(None, 'news', type_='foreignkey')
    # ### end Alembic commands ###
