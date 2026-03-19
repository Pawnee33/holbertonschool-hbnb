#!/usr/bin/python3

import unittest
from app.models.user import User
from app.models.place import Place


class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        self.owner = User("John", "Doe", "john@example.com")

    def test_place_creation_valid(self):
        place = Place(
            "Nice Place",
            "Description",
            100,
            45,
            3,
            self.owner
        )

        self.assertEqual(place.title, "Nice Place")
        self.assertEqual(place.price, 100)
        self.assertEqual(place.latitude, 45)
        self.assertEqual(place.longitude, 3)
        self.assertEqual(place.owner, self.owner)

    def test_title_required(self):
        with self.assertRaises(ValueError):
            Place("", "Desc", 100, 45, 3, self.owner)

    def test_title_too_long(self):
        with self.assertRaises(ValueError):
            Place("A" * 101, "Desc", 100, 45, 3, self.owner)

    def test_title_boundary_valid(self):
        place = Place("A" * 100, "Desc", 100, 45, 3, self.owner)
        self.assertEqual(len(place.title), 100)

    def test_price_must_be_positive(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", 0, 45, 3, self.owner)

    def test_price_negative(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", -10, 45, 3, self.owner)

    def test_price_type_invalid(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", "abc", 45, 3, self.owner)

    def test_latitude_above_boundary(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", 100, 91, 3, self.owner)

    def test_latitude_below_boundary(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", 100, -91, 3, self.owner)

    def test_latitude_boundary_valid(self):
        place = Place("Test", "Desc", 100, 90, 3, self.owner)
        self.assertEqual(place.latitude, 90)

    def test_longitude_above_boundary(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", 100, 45, 181, self.owner)

    def test_longitude_below_boundary(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", 100, 45, -181, self.owner)

    def test_longitude_boundary_valid(self):
        place = Place("Test", "Desc", 100, 45, 180, self.owner)
        self.assertEqual(place.longitude, 180)

    def test_owner_must_be_user_instance(self):
        with self.assertRaises(ValueError):
            Place("Test", "Desc", 100, 45, 3, "not-a-user")


if __name__ == '__main__':
    unittest.main()