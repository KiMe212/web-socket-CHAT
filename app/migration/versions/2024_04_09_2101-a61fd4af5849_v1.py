"""v1

Revision ID: a61fd4af5849
Revises:
Create Date: 2024-04-09 21:01:08.387644

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a61fd4af5849"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "room",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_room_id"), "room", ["id"], unique=False)
    op.create_table(
        "message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=True),
        sa.Column("status", sa.Enum("ONLINE", "LEFT", name="status"), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["room.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_message_id"), "message", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_message_id"), table_name="message")
    op.drop_table("message")
    op.drop_index(op.f("ix_room_id"), table_name="room")
    op.drop_table("room")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
