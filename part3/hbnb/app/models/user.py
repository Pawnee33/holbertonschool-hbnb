#!/usr/bin/python3
"""
User model.

This module defines the User entity which extends BaseModel and
represents an application user with validation rules for core fields.
"""


from app import bcrypt
from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates
import re


class User(BaseModel):
    """
    User domain model.

    Represents a user in the system with basic identity information
    and optional administrative privileges. Validation is performed
    during initialization to ensure data integrity.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("First name is required")
        if len(value) > 50:
            raise ValueError("First name must be 50 characters or less")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Last name is required")
        if len(value) > 50:
            raise ValueError("Last name must be 50 characters or less")
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Email is required")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        return value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

# Freeze blocks while waiting for task 9

#    def add_place(self, place):
#        """Add an amenity to the place."""
#        self.places.append(place)

#    def add_review(self, review):
#        """Add an amenity to the place."""
#        self.reviews.append(review)

#    def delete_review(self, review):
#        """Add an amenity to the place."""
#        self.reviews.remove(review)
