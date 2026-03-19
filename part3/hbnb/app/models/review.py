#!/usr/bin/python3

from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    """
    Class representing a review of a place by a user.

    Attributes:
        text (str): Text of the comment
        rating (int): Rating from 1 to 5
        place (Place): Place associated with the review
        user (User): User who wrote the review
    """

    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(
        db.Integer,
        db.CheckConstraint('rating >= 1 AND rating <= 5'),
        nullable=False
        )
    place_id = db.Column(
        db.String(36),
        db.ForeignKey('places.id'),
        nullable=False
        )
    place = db.relationship('Place', back_populates='reviews')
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
        )
    user = db.relationship('User', back_populates='reviews')

    @validates('text')
    def validate_text(self, key, value):
        if not value:
            raise ValueError("text is required")
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
