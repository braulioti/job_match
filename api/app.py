"""
Job Match API
Flask REST API for Job Match application
"""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.config.settings import Config
from api.database import init_db, db


def create_app(config_class=Config, run_migrations=True):
    """
    Create and configure the Flask application
    
    Args:
        config_class: Configuration class to use
        run_migrations: Whether to automatically run migrations on startup
                      (set to False when called from migration scripts)
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize database (basic setup)
    init_db(app)
    
    # Initialize Flask-Migrate (must be initialized before running migrations)
    Migrate(app, db)
    
    # Auto-run migrations on startup (unless disabled)
    if run_migrations:
        with app.app_context():
            try:
                from flask_migrate import upgrade
                upgrade()
                print("✓ Database migrations applied successfully")
            except Exception as e:
                print(f"⚠ Warning: Failed to run migrations automatically: {e}")
                import traceback
                traceback.print_exc()
                print("💡 You may need to run 'flask db upgrade' manually")
                # Fallback: create tables if migrations fail (development only)
                try:
                    db.create_all()
                    print("✓ Tables created using db.create_all() as fallback")
                except Exception as create_error:
                    print(f"✗ Error creating tables: {create_error}")
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'Job Match API'}, 200
    
    # Register blueprints
    from api.routes.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Register Swagger documentation
    try:
        from api.routes.swagger import SwaggerRoute
        swagger_route = SwaggerRoute()
        app.register_blueprint(swagger_route.blueprint)
        print("Swagger documentation registered at /docs")
        print(f"Swagger file path: {swagger_route.swagger_file_path}")
        print(f"Swagger file exists: {swagger_route.swagger_file_path.exists()}")
    except Exception as e:
        print(f"Warning: Failed to register Swagger documentation: {e}")
        import traceback
        traceback.print_exc()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
