"""
Upload API namespace.

This module defines the REST endpoint for uploading image files
to the server.
"""

import os
from flask import current_app
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

api = Namespace('upload', description='File upload operations')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/')
class Upload(Resource):
    @jwt_required()
    def post(self):
        """Upload an image file"""
        from flask import request
        if 'file' not in request.files:
            return {'error': 'No file provided'}, 400

        file = request.files['file']

        if file.filename == '':
            return {'error': 'No file selected'}, 400

        if not allowed_file(file.filename):
            return {'error': 'File type not allowed'}, 400

        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        return {'url': f'images/{filename}'}, 201
