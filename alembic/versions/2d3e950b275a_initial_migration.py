"""Initial migration

Revision ID: 2d3e950b275a
Revises: bb5668915e83
Create Date: 2024-07-16 23:47:29.276047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2d3e950b275a'
down_revision: Union[str, None] = 'bb5668915e83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_apps_id', table_name='apps')
    op.drop_table('apps')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('UUID', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('kind', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('version', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('state', postgresql.ENUM('new', 'installing', 'running', name='status'), autoincrement=False, nullable=True),
    sa.Column('json', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', 'UUID', name='apps_pkey'),
    sa.UniqueConstraint('UUID', name='apps_UUID_key')
    )
    op.create_index('ix_apps_id', 'apps', ['id'], unique=False)
    # ### end Alembic commands ###