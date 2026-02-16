"""make ip_address unique only for active records

Revision ID: df02fd50dc8c
Revises: 278cd52919b8
Create Date: 2026-02-15 19:48:01.839284

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'df02fd50dc8c'
down_revision = '278cd52919b8'
branch_labels = None
depends_on = None

def upgrade():
    # Удаляем старое уникальное ограничение
    op.drop_constraint('nas_devices_ip_address_key', 'nas_devices', type_='unique')
    # Создаём частичный уникальный индекс
    op.create_index('idx_nas_devices_ip_unique_active', 'nas_devices', ['ip_address'], unique=True, postgresql_where=sa.text('deleted_at IS NULL'))

def downgrade():
    # Откат: удаляем частичный индекс и восстанавливаем старое ограничение
    op.drop_index('idx_nas_devices_ip_unique_active', table_name='nas_devices')
    op.create_unique_constraint('nas_devices_ip_address_key', 'nas_devices', ['ip_address'])