"""payouts

Revision ID: 77f1e5ea4ac9
Revises: fd56b0a88c34
Create Date: 2023-10-10 10:33:01.655838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77f1e5ea4ac9'
down_revision: Union[str, None] = 'fd56b0a88c34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payouts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('on_date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payouts')
    # ### end Alembic commands ###