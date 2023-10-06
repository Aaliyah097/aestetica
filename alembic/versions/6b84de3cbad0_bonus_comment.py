"""bonus comment

Revision ID: 6b84de3cbad0
Revises: 7f449925422c
Create Date: 2023-10-05 12:59:51.328114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b84de3cbad0'
down_revision: Union[str, None] = '7f449925422c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bonuses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bonuses', schema=None) as batch_op:
        batch_op.drop_column('comment')

    # ### end Alembic commands ###
