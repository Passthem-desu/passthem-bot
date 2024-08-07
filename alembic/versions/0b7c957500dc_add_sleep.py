"""add sleep

Revision ID: 0b7c957500dc
Revises: b640fb1cd2c1
Create Date: 2024-07-04 23:10:24.706233

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0b7c957500dc"
down_revision: Union[str, None] = "b640fb1cd2c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_user_data", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "last_sleep_early_time", sa.Float(), server_default="0", nullable=False
            )
        )
        batch_op.add_column(
            sa.Column(
                "sleep_early_count", sa.Integer(), server_default="0", nullable=False
            )
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_user_data", schema=None) as batch_op:
        batch_op.drop_column("sleep_early_count")
        batch_op.drop_column("last_sleep_early_time")

    # ### end Alembic commands ###
