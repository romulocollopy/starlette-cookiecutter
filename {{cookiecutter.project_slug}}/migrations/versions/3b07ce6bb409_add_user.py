"""add user

Revision ID: 3b07ce6bb409
Revises:
Create Date: 2021-07-15 16:33:13.071716

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3b07ce6bb409"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.dialects.postgresql.UUID, primary_key=True),
        sa.Column("active", sa.Boolean, nullable=True),
        sa.Column("name", sa.String(50)),
        sa.Column("fullname", sa.String(50)),
        sa.Column("nickname", sa.String(12)),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.sql.func.now(),
        ),
        sa.Column(
            "updated_at", sa.DateTime, nullable=False, server_onupdate=sa.sql.func.now()
        ),
        sa.Index("id_active", "id", "active"),
    )


def downgrade():
    op.drop_table("users")
