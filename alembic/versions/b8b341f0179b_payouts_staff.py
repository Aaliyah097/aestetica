"""payouts staff

Revision ID: b8b341f0179b
Revises: 77f1e5ea4ac9
Create Date: 2023-10-10 17:26:28.017010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8b341f0179b'
down_revision: Union[str, None] = '77f1e5ea4ac9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payouts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('staff', sa.String(length=150), nullable=False))
        batch_op.create_foreign_key("staff", 'staff', ['staff'], ['name'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payouts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('staff')

    # ### end Alembic commands ###
