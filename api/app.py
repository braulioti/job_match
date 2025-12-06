"""
Job Match API
Flask REST API for Job Match application
"""

from flask import Flask
from flask_cors import CORS
from config.settings import Config


def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'Job Match API'}, 200
    
    # Register blueprints
    from routes.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Register Swagger documentation
    try:
        from routes.swagger import SwaggerRoute
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
