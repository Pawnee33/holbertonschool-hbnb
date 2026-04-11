#!/usr/bin/python3
"""
Place model.

This module defines the Place entity which represents a property
listed in the application. It includes location data, pricing,
ownership, and relationships with reviews and amenities.
"""


from app.models.basemodel import BaseModel
from app import db
from sqlalchemy.orm import validates
from app.models.amenity import Amenity
import json

place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
        ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True)
    )


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
    price = db.Column(
        db.Float,
        db.CheckConstraint('price > 0'),
        nullable=False
        )
    latitude = db.Column(
        db.Float,
        db.CheckConstraint('latitude >= -90 AND latitude <= 90'),
        nullable=False
        )
    longitude = db.Column(
        db.Float,
        db.CheckConstraint('longitude >= -180 AND longitude <= 180'),
        nullable=False
        )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
        )
    images = db.Column(
        db.Text, nullable=True,
        default='[]'
        )
    reviews = db.relationship(
        'Review',
        backref='place',
        lazy=True,
        cascade='all, delete-orphan'
    )
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

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

    def add_review(self, review):
        """
        Add a review to the place.

            review (Review): Review instance to associate with the place.

        Raises:
            ValueError: If review is not a valid Review instance.
        """
        from app.models.review import Review

        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        if review not in self.reviews:
            self.reviews.append(review)

    def delete_review(self, review):
        """Add an amenity to the place."""
        if review in self.reviews:
            self.reviews.remove(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.

        Args:
           amenity (Amenity): Amenity instance to associate with the place.

        Raises:
            ValueError: If amenity is not a valid Amenity instance.
        """
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    @validates('images')
    def validate_images(self, key, value):
        """
        Validate and normalize the images field.

        Accepts a list of URLs or a JSON string representing a list.
        Returns a JSON-encoded string for storage.

        Args:
            key (str): Field name being validated.
            value (list or str): Image URLs as a list or JSON string.

        Raises:
            ValueError: If value is not a valid list or JSON string.

        Returns:
            str: JSON-encoded list of image URLs.
        """
        if value is None:
            return '[]'
        if isinstance(value, list):
            return json.dumps(value)
        if isinstance(value, str):
            try:
                json.loads(value)
                return value
            except json.JSONDecodeError:
                raise ValueError("Images must be a valid JSON list")
        raise ValueError("Images must be a list or JSON string")

    def get_images(self):
        """
        Return the list of image URLs for this place.

        Returns:
            list: List of image URL strings.
        """
        if self.images:
            return json.loads(self.images)
        return []

    def set_images(self, image_list):
        """
        Store a list of image URLs as a JSON string.

        Args:
            image_list (list): List of image URL strings to store.
        """
        self.images = json.dumps(image_list)
