"""add tariff fields to user_profiles

Revision ID: <id2>
Revises: e06a5375d1d0
Create Date: 2026-02-16 12:30:00.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'acc269f91a95'
down_revision = 'e06a5375d1d0'   # важно: предыдущая миграция
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user_profiles', sa.Column('current_tariff_id', sa.Integer(), nullable=True))
    op.add_column('user_profiles', sa.Column('tariff_expires_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key('fk_user_profiles_tariff_id', 'user_profiles', 'tariff_plans', ['current_tariff_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_user_profiles_tariff_id', 'user_profiles', type_='foreignkey')
    op.drop_column('user_profiles', 'tariff_expires_at')
    op.drop_column('user_profiles', 'current_tariff_id')
