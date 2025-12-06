"""
API Routes
"""

from flask import Blueprint, jsonify, request

from api.controller.ia_controller import IAController

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'message': 'Job Match API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
        }
    }), 200


@api_bp.route('/ia/process', methods=['POST'])
def process():
    """
    Process data using AI/ML services

    Request body should contain:
    - data: The data to be processed
    - options: Optional processing options
    """
    data = request.get_json()
    response, status_code = IAController.process(data)
    return jsonify(response), status_code
