"""add broadcast

Revision ID: 393becfaaa91
Revises: 898044c4292d
Create Date: 2024-06-25 06:16:05.912823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "393becfaaa91"
down_revision: Union[str, None] = "898044c4292d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_global", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "last_reported_version", sa.String(), server_default="", nullable=False
            )
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_global", schema=None) as batch_op:
        batch_op.drop_column("last_reported_version")

    # ### end Alembic commands ###
