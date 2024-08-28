"""update award packs

Revision ID: 20240807T064740Z
Revises: 20240729T044728Z
Create Date: 2024-08-07 14:47:45.108955

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240807T064740Z"
down_revision: Union[str, None] = "20240729T044728Z"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_award", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("belong_pack", sa.String(), server_default="", nullable=False)
        )

    with op.batch_alter_table("catch_user_data", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("using_packs", sa.String(), server_default="", nullable=False)
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_user_data", schema=None) as batch_op:
        batch_op.drop_column("using_packs")

    with op.batch_alter_table("catch_award", schema=None) as batch_op:
        batch_op.drop_column("belong_pack")

    # ### end Alembic commands ###
