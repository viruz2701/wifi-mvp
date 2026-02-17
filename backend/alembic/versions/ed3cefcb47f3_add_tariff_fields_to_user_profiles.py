"""add tariff fields to user_profiles

Revision ID: acc269f91a95
Revises: e06a5375d1d0
Create Date: 2026-02-16 12:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ed3cefcb47f3'
down_revision = 'e06a5375d1d0'
branch_labels = None
depends_on = None

def upgrade():
    # Добавляем колонку current_tariff_id
    op.add_column('user_profiles', sa.Column('current_tariff_id', sa.Integer(), nullable=True))
    # Добавляем колонку tariff_expires_at
    op.add_column('user_profiles', sa.Column('tariff_expires_at', sa.DateTime(timezone=True), nullable=True))
    # Создаём внешний ключ
    op.create_foreign_key('fk_user_profiles_tariff_id', 'user_profiles', 'tariff_plans', ['current_tariff_id'], ['id'])

def downgrade():
    # Удаляем внешний ключ
    op.drop_constraint('fk_user_profiles_tariff_id', 'user_profiles', type_='foreignkey')
    # Удаляем колонки
    op.drop_column('user_profiles', 'tariff_expires_at')
    op.drop_column('user_profiles', 'current_tariff_id')
