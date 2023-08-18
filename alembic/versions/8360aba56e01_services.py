"""services

Revision ID: 8360aba56e01
Revises: cdca81c4f706
Create Date: 2023-08-18 10:29:00.881937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8360aba56e01'
down_revision: Union[str, None] = 'cdca81c4f706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('code', sa.String(length=20), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('code'),
    sa.UniqueConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    # ### end Alembic commands ###
