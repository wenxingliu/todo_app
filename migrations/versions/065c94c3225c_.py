"""empty message

Revision ID: 065c94c3225c
Revises: 1f08923fb42a
Create Date: 2020-12-11 22:12:51.822866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '065c94c3225c'
down_revision = '1f08923fb42a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('completed', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todo', 'completed')
    # ### end Alembic commands ###
