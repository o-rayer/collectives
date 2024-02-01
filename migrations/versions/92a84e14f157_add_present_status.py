"""Add present status

Revision ID: 92a84e14f157
Revises: 9226a31a5910
Create Date: 2023-05-08 14:41:13.493175

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "92a84e14f157"
down_revision = "9226a31a5910"
branch_labels = None
depends_on = None

before = sa.Enum(
    "Active",
    "Rejected",
    "PaymentPending",
    "SelfUnregistered",
    "JustifiedAbsentee",
    "UnJustifiedAbsentee",
    "Waiting",
)

after = sa.Enum(
    "Active",
    "Rejected",
    "PaymentPending",
    "SelfUnregistered",
    "JustifiedAbsentee",
    "UnJustifiedAbsentee",
    "Waiting",
    "Present",
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("registrations") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=before,
            type_=after,
            nullable=False,
        )
        before.name = "registrationstatus"
        after.name = "registrationstatus"
        batch_op.alter_column(
            "status",
            existing_type=before,
            type_=after,
            nullable=False,
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("registrations") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=after,
            type_=before,
            nullable=False,
        )

    # ### end Alembic commands ###
