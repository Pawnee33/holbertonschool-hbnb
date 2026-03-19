"""Facade is an intermediary between the API layer and
the persistance layer.
"""
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repositories.place_repository import PlaceRepository
from app.persistence.repositories.review_repository import ReviewRepository
from app.persistence.repositories.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    """HBnBFacade acts as an intermediary between the API layer and the
        persistence layer. It centralizes business logic and abstracts
        direct access to the repositories.
    """
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # USER
    def create_user(self, user_data):
        """create_user that create user"""
        user = User(**user_data)
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """get_user that retrieved an user"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """get_all_users that retrieved all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """update_user that update an user"""
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    def get_user_by_email(self, email):
        """get_user_by_email that retrieved an user via an email"""
        return self.user_repo.get_by_attribute('email', email)

    # PLACE
    def create_place(self, place_data):
        """Create a new place with validation"""

        try:
            owner_id = place_data["owner_id"]
            title = place_data["title"]
            description = place_data.get("description")
            price = place_data["price"]
            latitude = place_data["latitude"]
            longitude = place_data["longitude"]
            amenities_ids = place_data.get("amenities", [])
        except KeyError as e:
            raise ValueError(f"Missing field: {str(e)}")

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title,
            description,
            price,
            latitude,
            longitude,
            owner
        )

        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """get_place that retrieved place"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """get_all_places that retrieved all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """update_place that update a place"""
        place = self.get_place(place_id)
        if not place:
            return None

        place_data.pop("owner_id", None)
        place_data.pop("amenities", None)

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    def create_amenity(self, amenity_data):
        """
        Creates a new Amenity instance after
        validating the data provided.

        This method checks that the
        data entered is valid and contains the
        required fields before creating
        a new Amenity object. If the data
        is invalid or if required information
        is missing, a ValueError error is raised.

        Once validated, the Amenity instance
        is instantiated and stored in the
        internal amenities collection, then returned.
        """

        if not amenity_data or not isinstance(amenity_data, dict):
            raise ValueError("Invalid amenity data")
        if "name" not in amenity_data or not amenity_data["name"]:
            raise ValueError("Amenity name is required")
            
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    # AMENITY
    def get_amenity(self, amenity_id):

        """
        Retrieves a commodity from its identifier.

        Verifies that the identifier is valid and exists in
        memory storage before returning the corresponding object.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieves all amenities stored in the database.

        Performs a query to return all
        Amenity objects present in the database.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Updates an existing convenience.

        Searches for the convenience by its identifier, updates its
        attributes with the provided data, then saves the
        changes to the database.
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    # REVIEW
    def create_review(self, review_data):
        """
        Create a new review after validating the data.

        This method validates the data provided, verifies
        the existence of the associated user and location,
        then creates and saves a new review.

        Args:
        review_data (dict): Review data containing
            text, rating, user_id, and place_id.

        Returns:
        Review: Instance of the review created.

        Raises:
        ValueError: If the data is invalid, if a required field
        is missing, or if the user or place
        does not exist.
        """
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid input data')

        del review_data['user_id']
        review_data['user'] = user

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data')

        del review_data['place_id']
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by its ID.

        Args:
        review_id (int): Unique ID of the review.

        Returns:
        Review: Instance corresponding to the ID provided.

        Raises:
        ValueError: If the ID is invalid or if the
        review does not exist.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all saved reviews.

        Returns:
        list: List of all Review instances.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews associated with a given location.

        Args:
        place_id (str): Unique identifier for the location.

        Returns:
        list: List of reviews associated with the location.

        Raises:
        ValueError: If the location identifier is invalid
        or if the location does not exist.
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        """
        Update an existing review.

        This method updates only the authorized fields
        of a review, then saves the changes to the database.
    

        Args:
        review_id (int): Unique identifier of the review.
        review_data (dict): Data to be modified.

        Returns:
        Review: Updated instance.

        Raises:
        ValueError: If the review does not exist.
        """    
        review = self.get_review(review_id)
        if not review:
            return None

        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        """
        Delete an existing review.

        Args:
        review_id (int): Unique identifier of the review.

        Returns:
        bool: True if the deletion is successful.

        Raises:
        ValueError: If the review does not exist.
        """
        review = self.review_repo.get(review_id)
        
        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        user.delete_review(review)
        place.delete_review(review)
        self.review_repo.delete(review_id)
