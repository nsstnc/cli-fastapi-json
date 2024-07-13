"""Initial migration

Revision ID: bb5668915e83
Revises: 
Create Date: 2024-07-13 14:11:39.408979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb5668915e83'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('UUID', sa.String(), nullable=False),
    sa.Column('kind', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('state', sa.Enum('new', 'installing', 'running', name='status'), nullable=True),
    sa.Column('json', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'UUID'),
    sa.UniqueConstraint('UUID')
    )
    op.create_index(op.f('ix_apps_id'), 'apps', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_apps_id'), table_name='apps')
    op.drop_table('apps')
    # ### end Alembic commands ###
