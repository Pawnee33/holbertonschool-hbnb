"""
Application factory for the HBnB API.

This module provides the Flask application factory used to create
and configure the application instance, initialize the REST API,
and register all namespaces.
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
cors = CORS()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application.

    This factory initializes the Flask app instance, sets up the
    Flask-RESTX API with metadata and documentation endpoint,
    and registers all API namespaces.

    Returns:
        Flask: Configured Flask application instance.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'front', 'images')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.upload import api as upload_ns

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(upload_ns, path='/api/v1/upload')

    return app
