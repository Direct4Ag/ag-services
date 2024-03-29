"""new

Revision ID: 0906792b574b
Revises:
Create Date: 2024-01-03 19:42:50.497559+00:00

"""
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "0906792b574b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "farms",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("farm_name", sa.String(length=150), nullable=False),
        sa.Column("location_name", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "fields",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("field_name", sa.String(length=150), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POLYGON", from_text="ST_GeogFromText", name="geography"
            ),
            nullable=False,
        ),
        sa.Column("farm_ref_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["farm_ref_id"],
            ["farms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_fields_location",
        "fields",
        ["location"],
        unique=False,
        postgresql_using="gist",
    )
    op.create_table(
        "research",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("research_name", sa.String(length=200), nullable=False),
        sa.Column("research_area", sa.String(length=200), nullable=False),
        sa.Column("research_type", sa.String(length=200), nullable=False),
        sa.Column("field_ref_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["field_ref_id"],
            ["fields.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("research")
    op.drop_index("ix_fields_location", table_name="fields", postgresql_using="gist")
    op.drop_table("fields")
    op.drop_table("farms")
    # ### end Alembic commands ###
