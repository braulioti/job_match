"""
Migration environment configuration
"""

# Import Flask app and database
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables before creating app
from dotenv import load_dotenv
load_dotenv()

# Import database instance
from api.database.database import db

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import app factory
from api.app import create_app

# Create Flask app (without running migrations to avoid recursion)
# Pass run_migrations=False to prevent infinite loop
app = create_app(run_migrations=False)

# Always set database URL from Flask config
with app.app_context():
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    if database_url:
        config.set_main_option('sqlalchemy.url', database_url)
    
    # Import all models to ensure they are registered with SQLAlchemy metadata
    from api.models import models  # noqa: F401

# Set target metadata
target_metadata = db.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Get database URL - prefer explicit config, fallback to Flask app config
    database_url = config.get_main_option("sqlalchemy.url")
    if not database_url:
        with app.app_context():
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    
    if not database_url:
        raise ValueError(
            "No database URL configured. Please set DATABASE_URL environment variable "
            "or configure DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
        )
    
    # Create engine directly from URL
    from sqlalchemy import create_engine
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # Enable SQL execution in migrations
            include_schemas=True,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
