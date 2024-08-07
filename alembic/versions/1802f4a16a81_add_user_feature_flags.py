"""add user feature flags

Revision ID: 1802f4a16a81
Revises: ea9621ef4987
Create Date: 2024-06-22 01:53:48.830693

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1802f4a16a81"
down_revision: Union[str, None] = "ea9621ef4987"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_user_data", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "last_sign_in_time", sa.Float(), server_default="0", nullable=False
            )
        )
        batch_op.add_column(
            sa.Column("sign_in_count", sa.Integer(), server_default="0", nullable=False)
        )
        batch_op.add_column(
            sa.Column("feature_flag", sa.String(), server_default="", nullable=False)
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_user_data", schema=None) as batch_op:
        batch_op.drop_column("feature_flag")
        batch_op.drop_column("sign_in_count")
        batch_op.drop_column("last_sign_in_time")

    # ### end Alembic commands ###
