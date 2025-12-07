"""Create user table

Revision ID: 002_create_user_table
Revises: 001_create_file_table
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_create_user_table'
down_revision = '001_create_file_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create user table with all columns and indexes
    """
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('email', sa.String(length=255), nullable=False, comment='User email address'),
        sa.Column('password', sa.String(length=255), nullable=False, comment='Hashed password'),
        sa.Column('hash', sa.String(length=36), nullable=True, comment='UUID v4 hash for authentication'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.DateTime(), nullable=True, comment='Date and time of last login'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uq_user_email'),
        sa.UniqueConstraint('hash', name='uq_user_hash')
    )
    
    # Create indexes
    op.create_index('idx_user_email', 'user', ['email'], unique=True)
    op.create_index('idx_user_hash', 'user', ['hash'], unique=True)
    op.create_index('idx_user_created_at', 'user', ['created_at'], unique=False)


def downgrade() -> None:
    """
    Drop user table and all related objects
    """
    
    # Drop indexes
    op.drop_index('idx_user_created_at', table_name='user')
    op.drop_index('idx_user_hash', table_name='user')
    op.drop_index('idx_user_email', table_name='user')
    
    # Drop table (this will also drop the unique constraints)
    op.drop_table('user')
