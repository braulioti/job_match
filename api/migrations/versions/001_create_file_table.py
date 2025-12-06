"""Create file table

Revision ID: 001_create_file_table
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_create_file_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create file table with all columns, indexes, and triggers
    """
    # Create file table
    op.create_table(
        'file',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('original_file_name', sa.String(length=200), nullable=False, comment='Original name of the uploaded file'),
        sa.Column('hash', sa.String(length=40), nullable=False, comment='SHA-1 hash of the file content'),
        sa.Column('extension', sa.String(length=15), nullable=True, comment='File extension (e.g., .pdf, .docx)'),
        sa.Column('content', sa.Text(), nullable=True, comment='Full text content converted to TXT'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hash', name='uq_file_hash')
    )
    
    # Create indexes using Alembic op (more reliable than SQL direct)
    op.create_index('idx_file_created_at', 'file', ['created_at'], unique=False)
    
    # Partial index for extension (only non-null values)
    op.execute('''
        CREATE INDEX IF NOT EXISTS idx_file_extension 
        ON file(extension) 
        WHERE extension IS NOT NULL;
    ''')


def downgrade() -> None:
    """
    Drop file table and all related objects
    """
    
    # Drop indexes (use op.drop_index for better tracking)
    op.execute('DROP INDEX IF EXISTS idx_file_extension;')
    op.drop_index('idx_file_created_at', table_name='file')
    
    # Drop table (this will also drop the unique constraint)
    op.drop_table('file')

