"""update user call

Revision ID: 20240729T044728Z
Revises: 20240713T094332Z
Create Date: 2024-07-29 12:47:32.081618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20240729T044728Z'
down_revision: Union[str, None] = '20240713T094332Z'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('catch_user_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('special_call', sa.String(), server_default='', nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('catch_user_data', schema=None) as batch_op:
        batch_op.drop_column('special_call')

    # ### end Alembic commands ###