"""Initial

Revision ID: a2febb75703c
Revises: 
Create Date: 2021-07-26 07:47:07.881293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2febb75703c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.String(length=36), nullable=True),
    sa.Column('original_file_name', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('md5_hash', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_info')
    # ### end Alembic commands ###