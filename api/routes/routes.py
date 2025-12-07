"""
API Routes
"""

from flask import Blueprint, jsonify, request

from api.controller.ia_controller import IAController
from api.controller.file_controller import FileController
from api.controller.user_controller import UserController

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


@api_bp.route('/file', methods=['POST'])
def upload_file():
    """
    Upload a file
    
    Request should contain:
    - file: The file to be uploaded (multipart/form-data)
    
    Returns:
    - File information including ID, hash, and metadata
    """
    if 'file' not in request.files:
        return jsonify({
            'error': 'Bad request',
            'message': 'No file provided'
        }), 400
    
    file = request.files['file']
    response, status_code = FileController.upload_file(file)
    return jsonify(response), status_code


@api_bp.route('/user', methods=['POST'])
def create_user():
    """
    Create a new user
    
    Request body should contain:
    - email: User email address
    - password: User password
    
    Returns:
    - User information including ID, email, and creation date
    """
    data = request.get_json()
    response, status_code = UserController.create_user(data)
    return jsonify(response), status_code
