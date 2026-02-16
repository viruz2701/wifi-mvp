"""add method to sms_codes

Revision ID: 2afedea6208d
Revises: df02fd50dc8c
Create Date: 2026-02-16 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2afedea6208d'
down_revision = 'df02fd50dc8c'
branch_labels = None
depends_on = None

def upgrade():
    # Сначала создаём enum тип
    smsprovidertype = sa.Enum('ROCKETSMS', 'CALLPASSWORD', name='smsprovidertype')
    smsprovidertype.create(op.get_bind(), checkfirst=True)
    
    # Добавляем колонку type, используя созданный enum
    op.add_column('sms_providers', sa.Column('type', smsprovidertype, nullable=False, server_default='ROCKETSMS'))
    
    # Делаем колонку config NOT NULL (если нужно)
    op.alter_column('sms_providers', 'config',
               existing_type=sa.JSON(),
               nullable=False)
    
    # Удаляем старые колонки
    op.drop_column('sms_providers', 'api_url')
    op.drop_column('sms_providers', 'api_key')
    op.drop_column('sms_providers', 'sender')
    
    # Создаём уникальное ограничение на ip_address в nas_devices
    op.create_unique_constraint(None, 'nas_devices', ['ip_address'])

def downgrade():
    # Удаляем уникальное ограничение
    op.drop_constraint('nas_devices_ip_address_key', 'nas_devices', type_='unique')
    
    # Возвращаем старые колонки
    op.add_column('sms_providers', sa.Column('sender', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('sms_providers', sa.Column('api_key', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('sms_providers', sa.Column('api_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    
    # Удаляем колонку type
    op.drop_column('sms_providers', 'type')
    
    # Удаляем enum тип
    smsprovidertype = sa.Enum(name='smsprovidertype')
    smsprovidertype.drop(op.get_bind(), checkfirst=True)