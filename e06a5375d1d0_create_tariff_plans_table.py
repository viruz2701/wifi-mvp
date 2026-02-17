"""create tariff_plans table

Revision ID: e06a5375d1d0
Revises: 6bfafcee1360
Create Date: 2026-02-16 12:09:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'e06a5375d1d0'
down_revision = '6bfafcee1360'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('tariff_plans',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('duration_hours', sa.Integer(), nullable=False),
        sa.Column('speed_limit_up_kbps', sa.Integer(), nullable=True),
        sa.Column('speed_limit_down_kbps', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tariff_plans_id'), 'tariff_plans', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_tariff_plans_id'), table_name='tariff_plans')
    op.drop_table('tariff_plans')
