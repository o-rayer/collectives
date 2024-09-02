"""add registration time

Revision ID: 01e5792cdfac
Revises: bf9a9943d273
Create Date: 2024-08-13 09:01:39.629596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e5792cdfac'
down_revision = 'bf9a9943d273'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('badges', schema=None) as batch_op:
        batch_op.alter_column('badge_id',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.Enum('Benevole', 'LateUnregisterWarning', 'Banned', name='badgeids'),
               existing_nullable=False)

    # with op.batch_alter_table('config', schema=None) as batch_op:
    #     batch_op.alter_column('type',
    #            existing_type=sa.VARCHAR(length=11),
    #            nullable=True)

    # with op.batch_alter_table('equipments', schema=None) as batch_op:
    #     batch_op.drop_index('ix_equipments_purchaseDate')
    #     batch_op.create_index(batch_op.f('ix_equipments_purchase_date'), ['purchase_date'], unique=False)

    # with op.batch_alter_table('events', schema=None) as batch_op:
    #     batch_op.alter_column('event_type_id',
    #            existing_type=sa.INTEGER(),
    #            nullable=True,
    #            existing_server_default=sa.text("'1'"))
    #     batch_op.create_foreign_key(None, 'users', ['main_leader_id'], ['id'])

    # with op.batch_alter_table('group_event_conditions', schema=None) as batch_op:
    #     batch_op.drop_constraint(None, type_='foreignkey')

    # with op.batch_alter_table('payments', schema=None) as batch_op:
    #     batch_op.drop_index('ix_payments_creditor_id')
    #     batch_op.create_index(batch_op.f('ix_payments_buyer_id'), ['buyer_id'], unique=False)

    with op.batch_alter_table('registrations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registration_time', sa.DateTime(), nullable=True))
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=19),
               type_=sa.Enum('Active', 'Rejected', 'PaymentPending', 'SelfUnregistered', 'JustifiedAbsentee', 'UnJustifiedAbsentee', 'ToBeDeleted', 'Waiting', 'Present', 'LateSelfUnregistered', name='registrationstatus'),
               existing_nullable=False)
        batch_op.create_index(batch_op.f('ix_registrations_registration_time'), ['registration_time'], unique=False)

    # with op.batch_alter_table('users', schema=None) as batch_op:
    #     batch_op.alter_column('type',
    #            existing_type=sa.VARCHAR(length=16),
    #            type_=sa.Enum('Test', 'Extranet', 'Local', 'UnverifiedLocal', name='usertype'),
    #            existing_nullable=False,
    #            existing_server_default=sa.text("'Test'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # with op.batch_alter_table('users', schema=None) as batch_op:
    #     batch_op.alter_column('type',
    #            existing_type=sa.Enum('Test', 'Extranet', 'Local', 'UnverifiedLocal', name='usertype'),
    #            type_=sa.VARCHAR(length=16),
    #            existing_nullable=False,
    #            existing_server_default=sa.text("'Test'"))

    with op.batch_alter_table('registrations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_registrations_registration_time'))
        batch_op.alter_column('status',
               existing_type=sa.Enum('Active', 'Rejected', 'PaymentPending', 'SelfUnregistered', 'JustifiedAbsentee', 'UnJustifiedAbsentee', 'ToBeDeleted', 'Waiting', 'Present', 'LateSelfUnregistered', name='registrationstatus'),
               type_=sa.VARCHAR(length=19),
               existing_nullable=False)
        batch_op.drop_column('registration_time')

    # with op.batch_alter_table('payments', schema=None) as batch_op:
    #     batch_op.drop_index(batch_op.f('ix_payments_buyer_id'))
    #     batch_op.create_index('ix_payments_creditor_id', ['buyer_id'], unique=False)

    # with op.batch_alter_table('group_event_conditions', schema=None) as batch_op:
    #     batch_op.create_foreign_key(None, 'activity_types', ['event_id'], ['id'])

    # with op.batch_alter_table('events', schema=None) as batch_op:
    #     batch_op.drop_constraint(None, type_='foreignkey')
    #     batch_op.alter_column('event_type_id',
    #            existing_type=sa.INTEGER(),
    #            nullable=False,
    #            existing_server_default=sa.text("'1'"))

    # with op.batch_alter_table('equipments', schema=None) as batch_op:
    #     batch_op.drop_index(batch_op.f('ix_equipments_purchase_date'))
    #     batch_op.create_index('ix_equipments_purchaseDate', ['purchase_date'], unique=False)

    # with op.batch_alter_table('config', schema=None) as batch_op:
    #     batch_op.alter_column('type',
    #            existing_type=sa.VARCHAR(length=11),
    #            nullable=False)

    with op.batch_alter_table('badges', schema=None) as batch_op:
        batch_op.alter_column('badge_id',
               existing_type=sa.Enum('Benevole', 'LateUnregisterWarning', 'Banned', name='badgeids'),
               type_=sa.VARCHAR(length=8),
               existing_nullable=False)

    # ### end Alembic commands ###