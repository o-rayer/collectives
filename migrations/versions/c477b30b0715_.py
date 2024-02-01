"""empty message

Revision ID: c477b30b0715
Revises:
Create Date: 2020-02-08 01:05:17.875387

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = "c477b30b0715"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "activity_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("short", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("rendered_description", sa.Text(), nullable=True),
        sa.Column("photo", sa.String(length=100), nullable=True),
        sa.Column("start", sa.DateTime(), nullable=False),
        sa.Column("end", sa.DateTime(), nullable=False),
        sa.Column("num_slots", sa.Integer(), nullable=False),
        sa.Column("num_online_slots", sa.Integer(), nullable=False),
        sa.Column("registration_open_time", sa.DateTime(), nullable=True),
        sa.Column("registration_close_time", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("Confirmed", "Pending", "Cancelled", name="eventstatus"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_start"), "events", ["start"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_test", sa.Boolean(), nullable=False),
        sa.Column("mail", sa.String(length=100), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("license", sa.String(length=100), nullable=False),
        sa.Column("license_category", sa.String(length=2), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column(
            "password",
            sqlalchemy_utils.types.password.PasswordType(max_length=1137),
            nullable=True,
        ),
        sa.Column("avatar", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("emergency_contact_name", sa.String(length=100), nullable=False),
        sa.Column("emergency_contact_phone", sa.String(length=20), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("license_expiry_date", sa.Date(), nullable=True),
        sa.Column("last_extranet_sync_time", sa.DateTime(), nullable=True),
        sa.Column(
            "gender",
            sa.Enum("Unknown", "Woman", "Man", "Other", name="gender"),
            nullable=False,
        ),
        sa.Column("last_failed_login", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_license"), "users", ["license"], unique=True)
    op.create_index(op.f("ix_users_mail"), "users", ["mail"], unique=True)
    op.create_table(
        "confirmation_token",
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("expiry_date", sa.DateTime(), nullable=False),
        sa.Column("user_license", sa.String(length=12), nullable=False),
        sa.Column("existing_user_id", sa.Integer(), nullable=True),
        sa.Column(
            "token_type",
            sa.Enum("ActivateAccount", "RecoverAccount", name="confirmationtokentype"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["existing_user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "event_activity_types",
        sa.Column("activity_id", sa.Integer(), nullable=True),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activity_types.id"],
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
    )
    op.create_index(
        op.f("ix_event_activity_types_activity_id"),
        "event_activity_types",
        ["activity_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_event_activity_types_event_id"),
        "event_activity_types",
        ["event_id"],
        unique=False,
    )
    op.create_table(
        "event_leaders",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
    )
    op.create_index(
        op.f("ix_event_leaders_event_id"), "event_leaders", ["event_id"], unique=False
    )
    op.create_index(
        op.f("ix_event_leaders_user_id"), "event_leaders", ["user_id"], unique=False
    )
    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("Active", "Rejected", name="registrationstatus"),
            nullable=False,
        ),
        sa.Column(
            "level",
            sa.Enum("Normal", "CoLeader", name="registrationlevels"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_registrations_event_id"), "registrations", ["event_id"], unique=False
    )
    op.create_index(
        op.f("ix_registrations_user_id"), "registrations", ["user_id"], unique=False
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("activity_id", sa.Integer(), nullable=True),
        sa.Column(
            "role_id",
            sa.Enum(
                "Moderator",
                "Administrator",
                "President",
                "EventLeader",
                "ActivitySupervisor",
                name="roleids",
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activity_types.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_roles_user_id"), "roles", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_roles_user_id"), table_name="roles")
    op.drop_table("roles")
    op.drop_index(op.f("ix_registrations_user_id"), table_name="registrations")
    op.drop_index(op.f("ix_registrations_event_id"), table_name="registrations")
    op.drop_table("registrations")
    op.drop_index(op.f("ix_event_leaders_user_id"), table_name="event_leaders")
    op.drop_index(op.f("ix_event_leaders_event_id"), table_name="event_leaders")
    op.drop_table("event_leaders")
    op.drop_index(
        op.f("ix_event_activity_types_event_id"), table_name="event_activity_types"
    )
    op.drop_index(
        op.f("ix_event_activity_types_activity_id"), table_name="event_activity_types"
    )
    op.drop_table("event_activity_types")
    op.drop_table("confirmation_token")
    op.drop_index(op.f("ix_users_mail"), table_name="users")
    op.drop_index(op.f("ix_users_license"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_events_start"), table_name="events")
    op.drop_table("events")
    op.drop_table("activity_types")
    # ### end Alembic commands ###
