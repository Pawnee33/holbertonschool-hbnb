#!/usr/bin/python3

from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """
    The Amenity class extends BaseModel, inheriting common attributes such as:
    id (UUID)
    created_at
    updated_at

    The constructor ensures data integrity 
    by validating the name attribute:
    It checks that a name is provided.
    It ensures the name does not exceed 50 characters.
    It raises a ValueError if validation fails.
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")

        if not value:
            raise ValueError("Name is required")

        if len(value) > 50:
            raise ValueError("Name must be 50 characters or less")
        return value
