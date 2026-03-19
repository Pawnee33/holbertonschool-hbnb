#!/usr/bin/python3
"""
User model.

This module defines the User entity which extends BaseModel and
represents an application user with validation rules for core fields.
"""


from app.models.base_model import BaseModel
import re


class User(BaseModel):
    """
    User domain model.

    Represents a user in the system with basic identity information
    and optional administrative privileges. Validation is performed
    during initialization to ensure data integrity.
    """

    emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance.

        Validates required fields and constraints such as maximum
        length for names and basic email format.

        Args:
            first_name (str): User's first name (required, max 50 characters).
            last_name (str): User's last name (required, max 50 characters).
            email (str): User's email address (required, must be valid format).
            is_admin (bool, optional): Indicates whether the user has
                administrative privileges. Defaults to False.

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("First name is required")
        if len(value) > 50:
            raise ValueError("First name must be 50 characters or less")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Last name is required")
        if len(value) > 50:
            raise ValueError("Last name must be 50 characters or less")
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise ValueError("Email is required")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")

        self.__email = value

    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self.__is_admin = value

    def add_place(self, place):
        """Add an amenity to the place."""
        self.places.append(place)

    def add_review(self, review):
        """Add an amenity to the place."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)
