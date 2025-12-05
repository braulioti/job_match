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
    
    # Register blueprints
    from routes.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'Job Match API'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
