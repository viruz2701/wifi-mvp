"""add method, call_id, provider_id to sms_codes

Revision ID: 34e418709a70
Revises: 2afedea6208d
Create Date: 2026-02-16 14:32:18.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '34e418709a70'
down_revision = '2afedea6208d'
branch_labels = None
depends_on = None

def upgrade():
    # Сначала создаём enum тип для method
    codemethod = sa.Enum('SMS', 'CALL', name='codemethod')
    codemethod.create(op.get_bind(), checkfirst=True)
    
    # Добавляем колонки
    op.add_column('sms_codes', sa.Column('method', codemethod, nullable=False, server_default='SMS'))
    op.add_column('sms_codes', sa.Column('call_id', sa.String(), nullable=True))
    op.add_column('sms_codes', sa.Column('provider_id', sa.Integer(), nullable=True))
    
    # Создаём внешний ключ
    op.create_foreign_key(None, 'sms_codes', 'sms_providers', ['provider_id'], ['id'])

def downgrade():
    # Удаляем внешний ключ
    op.drop_constraint('sms_codes_provider_id_fkey', 'sms_codes', type_='foreignkey')
    
    # Удаляем колонки
    op.drop_column('sms_codes', 'provider_id')
    op.drop_column('sms_codes', 'call_id')
    op.drop_column('sms_codes', 'method')
    
    # Удаляем enum тип
    codemethod = sa.Enum(name='codemethod')
    codemethod.drop(op.get_bind(), checkfirst=True)