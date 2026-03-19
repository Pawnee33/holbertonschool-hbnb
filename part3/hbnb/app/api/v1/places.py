"""
User API namespace.

This module defines REST endpoints for managing places, including
creation, retrieval, and update operations. It relies on a facade
service layer to handle business logic and data persistence.
"""


from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place'
    ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place'
    ),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(
        fields.String, required=True,
        description="List of amenities ID's"
    )
})


@api.route('/')
class PlaceList(Resource):
    """
    Resource for operations on the place collection.

    Provides endpoints to create a new place and to retrieve
    the list of all places.
    """
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload

        current_user = get_jwt_identity()

        place_data["owner_id"] = current_user

        try:
            new_place = facade.create_place(place_data)
        except ValueError as error:
            return {'error': str(error)}, 400
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner.id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        list_places = []
        for place in places:
            list_places.append({
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            })
        return list_places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                }
                for amenity in place.amenities
            ]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id != current_user:
            return {"error": "Unauthorized action"}, 403
        try:
            update_place = facade.update_place(place_id, place_data)
        except ValueError as error:
            return {'error': str(error)}, 400
        return {
            'id': update_place.id,
            'title': update_place.title,
            'description': update_place.description,
            'price': update_place.price,
            'latitude': update_place.latitude,
            'longitude': update_place.longitude,
            'owner_id': update_place.owner.id
        }, 200

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        amenities_data = api.payload
        if not amenities_data or len(amenities_data) == 0:
            return {'error': 'Invalid input data'}, 400
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        for amenity in amenities_data:
            a = facade.get_amenity(amenity['id'])
            if not a:
                return {'error': 'Invalid input data'}, 400
        
        for amenity in amenities_data:
            place.add_amenity(a)
        return {'message': 'Amenities added successfully'}, 200

@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = place.reviews

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place.id,
                'user_id': review.user.id
            }
            for review in reviews
        ], 200
