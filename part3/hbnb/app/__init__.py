"""
Application factory for the HBnB API.

This module provides the Flask application factory used to create
and configure the application instance, initialize the REST API,
and register all namespaces.
"""


from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()


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


    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

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

    return app
