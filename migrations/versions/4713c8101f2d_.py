"""empty message

Revision ID: 4713c8101f2d
Revises: a6fbf32aa541
Create Date: 2019-11-23 19:44:08.029904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4713c8101f2d'
down_revision = 'a6fbf32aa541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('img_url', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'img_url')
    # ### end Alembic commands ###