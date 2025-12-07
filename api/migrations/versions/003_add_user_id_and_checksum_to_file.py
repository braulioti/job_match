"""Add user_id and checksum to file table

Revision ID: 003_add_user_id_and_checksum_to_file
Revises: 002_create_user_table
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003_add_user_id_and_checksum_to_file'
down_revision = '002_create_user_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add user_id foreign key and checksum column to file table
    """
    # Add user_id column with foreign key constraint
    op.add_column('file', sa.Column('user_id', sa.Integer(), nullable=True, comment='Foreign key to user table'))
    op.create_foreign_key('fk_file_user_id', 'file', 'user', ['user_id'], ['id'], ondelete='SET NULL')
    
    # Add checksum column
    op.add_column('file', sa.Column('checksum', sa.String(length=255), nullable=True, comment='Hash for file validation'))
    
    # Create indexes
    op.create_index('idx_file_user_id', 'file', ['user_id'], unique=False)
    op.create_index('idx_file_checksum', 'file', ['checksum'], unique=False)


def downgrade() -> None:
    """
    Remove user_id and checksum columns from file table
    """
    
    # Drop indexes
    op.drop_index('idx_file_checksum', table_name='file')
    op.drop_index('idx_file_user_id', table_name='file')
    
    # Drop foreign key constraint
    op.drop_constraint('fk_file_user_id', 'file', type_='foreignkey')
    
    # Drop columns
    op.drop_column('file', 'checksum')
    op.drop_column('file', 'user_id')
