#!/usr/bin/python3
"""
Place model.

This module defines the Place entity which represents a property
listed in the application. It includes location data, pricing,
ownership, and relationships with reviews and amenities.
"""


from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

# Freeze blocks while waiting for task 9

#from app.models.user import User
#from app.models.amenity import Amenity


class Place(BaseModel):
    """
    Place domain model.

    Represents a property that can be listed by a user. A place
    includes descriptive information, geographic coordinates,
    pricing, an owner, and collections of reviews and amenities.
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, db.CheckConstraint('price > 0'), nullable=False)
    latitude = db.Column(db.Float, db.CheckConstraint('latitude >= -90 AND latitude <= 90'), nullable=False)
    longitude = db.Column(db.Float, db.CheckConstraint('longitude >= -180 AND longitude <= 180'), nullable=False)

    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title is required")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters or less")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be an integer or a float")
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if value is None or not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

# Freeze blocks while waiting for task 9
 
#    @property
#   def owner(self):
#        return self.__owner

#    @owner.setter
#    def owner(self, value):
#        if not isinstance(value, User):
#            raise ValueError("Owner must be a User instance")
#        self.__owner = value

#    def add_review(self, review):
#        """
#        Add a review to the place.

#        Args:
#            review (Review): Review instance to associate with the place.

#        Raises:
#            ValueError: If review is not a valid Review instance.
#        """
#        from app.models.review import Review

#        if not isinstance(review, Review):
#            raise ValueError("review must be a Review instance")
#        if review not in self.reviews:
#            self.reviews.append(review)

#    def delete_review(self, review):
#        """Add an amenity to the place."""
#        self.reviews.remove(review)

#    def add_amenity(self, amenity):
#        """
#        Add an amenity to the place.

#        Args:
#           amenity (Amenity): Amenity instance to associate with the place.

#        Raises:
#            ValueError: If amenity is not a valid Amenity instance.
#        """
#        if not isinstance(amenity, Amenity):
#            raise ValueError("amenity must be an Amenity instance")
#        if amenity not in self.amenities:
#            self.amenities.append(amenity)
