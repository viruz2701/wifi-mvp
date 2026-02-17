"""add settings table

Revision ID: 07d0c3e4317c
Revises: 3e143d363f79   # замените, если другая
Create Date: 2026-02-16 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '07d0c3e4317c'
down_revision = '3e143d363f79'  # проверьте через alembic current
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('settings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.create_index(op.f('ix_settings_id'), 'settings', ['id'], unique=False)
    op.create_index(op.f('ix_settings_key'), 'settings', ['key'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_settings_key'), table_name='settings')
    op.drop_index(op.f('ix_settings_id'), table_name='settings')
    op.drop_table('settings')
