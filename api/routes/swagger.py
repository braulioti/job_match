"""
Swagger Documentation Route
Handles Swagger UI rendering
"""

from pathlib import Path

import yaml
from flask import Blueprint, jsonify


class SwaggerRoute:
    """Class to handle Swagger documentation routes"""
    
    def __init__(self, swagger_file_path=None):
        """
        Initialize Swagger route handler
        
        Args:
            swagger_file_path: Path to the Swagger YAML file. If None, uses default path.
        """
        if swagger_file_path is None:
            # Default path: api/swagger/pt-BR.yaml
            # __file__ is api/routes/swagger.py
            # parent.parent goes to api/
            base_path = Path(__file__).parent.parent.resolve()
            self.swagger_file_path = (base_path / 'swagger' / 'pt-BR.yaml').resolve()
        else:
            base_path = None
            self.swagger_file_path = Path(swagger_file_path).resolve()
        
        # Verify file exists
        if not self.swagger_file_path.exists():
            print(f"Warning: Swagger file not found at {self.swagger_file_path}")
            print(f"Current working directory: {Path.cwd()}")
            if base_path:
                print(f"Base path: {base_path}")
            print(f"Looking for file: {self.swagger_file_path.absolute()}")
        
        self.blueprint = Blueprint('swagger', __name__, url_prefix='')
        self._register_routes()
    
    def _register_routes(self):
        """Register all Swagger-related routes"""
        
        @self.blueprint.route('/docs')
        def swagger_ui():
            """Render Swagger UI"""
            return self._render_swagger_ui()
        
        @self.blueprint.route('/docs/swagger.json')
        def swagger_json():
            """Return Swagger specification as JSON"""
            return self._get_swagger_json()
        
        @self.blueprint.route('/docs/swagger.yaml')
        def swagger_yaml():
            """Return Swagger specification as YAML"""
            return self._get_swagger_yaml()
    
    def _render_swagger_ui(self):
        """Render Swagger UI HTML page"""
        swagger_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Match API - Documentação</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui.css" />
    <style>
        html {{
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }}
        *, *:before, *:after {{
            box-sizing: inherit;
        }}
        body {{
            margin:0;
            background: #fafafa;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: "/docs/swagger.yaml",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null,
                defaultModelsExpandDepth: 1,
                defaultModelExpandDepth: 1,
                docExpansion: "list",
                filter: true,
                showExtensions: true,
                showCommonExtensions: true
            }})
        }}
    </script>
</body>
</html>
"""
        from flask import Response
        return Response(swagger_html, mimetype='text/html')
    
    def _get_swagger_json(self):
        """Load and return Swagger specification as JSON"""
        try:
            with open(self.swagger_file_path, 'r', encoding='utf-8') as f:
                swagger_data = yaml.safe_load(f)
            return jsonify(swagger_data)
        except FileNotFoundError:
            return jsonify({'error': 'Swagger file not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Error loading Swagger file: {str(e)}'}), 500
    
    def _get_swagger_yaml(self):
        """Load and return Swagger specification as YAML"""
        try:
            if not self.swagger_file_path.exists():
                error_msg = {
                    'error': 'Swagger file not found',
                    'path': str(self.swagger_file_path),
                    'absolute_path': str(self.swagger_file_path.absolute()),
                    'cwd': str(Path.cwd())
                }
                return jsonify(error_msg), 404
            
            with open(self.swagger_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            from flask import Response
            return Response(content, mimetype='text/yaml; charset=utf-8')
        except FileNotFoundError:
            error_msg = {
                'error': 'Swagger file not found',
                'path': str(self.swagger_file_path),
                'absolute_path': str(self.swagger_file_path.absolute())
            }
            return jsonify(error_msg), 404
        except Exception as e:
            import traceback
            error_msg = {
                'error': f'Error loading Swagger file: {str(e)}',
                'path': str(self.swagger_file_path),
                'traceback': traceback.format_exc()
            }
            return jsonify(error_msg), 500

