"""
User API namespace.

This module defines REST endpoints for managing users, including
creation, retrieval, and update operations. It relies on a facade
service layer to handle business logic and data persistence.
"""


from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password'),

})

@api.route('/')
class UserList(Resource):
    """
    Resource for operations on the user collection.

    Provides endpoints to create a new user and to retrieve
    the list of all users.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new user.

        Validates input data against the user model, checks
        that the email is unique, and creates the user via
        the service facade.

        Returns:
            tuple: JSON representation of the created user and HTTP status code.
        """
        claims = get_jwt()

        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': new_user.id,
            "message": "User created successfully"
        }, 201

    @api.response(200, 'User details retrieved successfully')
    def get(self):
        """
        Retrieve all users.

        Fetches the complete list of users from the service
        layer and returns them as a JSON array.

        Returns:
            tuple: List of users and HTTP status code.
        """
        users = facade.get_all_users()
        List_user = []
        for user in users:
            List_user.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
        return List_user, 200


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for operations on a single user.

    Provides endpoints to retrieve and update a user
    identified by their unique ID.
    """
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            tuple: User data if found, otherwise an error message and status code.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user.

        Validates the input payload and updates the user
        through the service facade.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            tuple: Updated user data if successful, otherwise an error message.
        """
        data_user = api.payload

        claims = get_jwt()
        current_user = get_jwt_identity()

        is_admin = claims.get("is_admin", False)

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if not is_admin and user_id != current_user:
            return {"error": "Unauthorized action"}, 403

        if not is_admin and "email" in data_user or "password" in data_user:
            return {"error": "You cannot modify email or password"}, 400

        if "email" in data_user:
            existing = facade.get_user_by_email(data_user["email"])
            if existing and existing.id != user_id:
                return {"error": "Email already registered"}, 400

        try:
            update_user = facade.update_user(user_id, data_user)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {
            'id': update_user.id,
            'first_name': update_user.first_name,
            'last_name': update_user.last_name,
            'email': update_user.email
        }, 200
