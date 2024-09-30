"""empty message

Revision ID: 6075b4bc9756
Revises: 
Create Date: 2024-09-30 15:06:39.219190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6075b4bc9756'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
