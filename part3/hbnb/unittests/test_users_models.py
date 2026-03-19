#!/usr/bin/python3

import unittest
from app.models.user import User


class TestUserModel(unittest.TestCase):

    def test_user_creation_valid(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )

        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)

    def test_first_name_required(self):
        with self.assertRaises(ValueError):
            User("", "Doe", "john@example.com")

    def test_first_name_too_long(self):
        with self.assertRaises(ValueError):
            User("A" * 51, "Doe", "john@example.com")

    def test_first_name_boundary_valid(self):
        user = User("A" * 50, "Doe", "john@example.com")
        self.assertEqual(len(user.first_name), 50)

    def test_last_name_required(self):
        with self.assertRaises(ValueError):
            User("John", "", "john@example.com")

    def test_last_name_too_long(self):
        with self.assertRaises(ValueError):
            User("John", "B" * 51, "john@example.com")

    def test_last_name_boundary_valid(self):
        user = User("John", "B" * 50, "john@example.com")
        self.assertEqual(len(user.last_name), 50)

    def test_email_required(self):
        with self.assertRaises(ValueError):
            User("John", "Doe", "")

    def test_invalid_email_format(self):
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid-email")

    def test_valid_email_formats(self):
        valid_emails = [
            "a@b.com",
            "john.doe@test.co",
            "user123@mail-domain.org"
        ]

        for email in valid_emails:
            user = User("John", "Doe", email)
            self.assertEqual(user.email, email)


if __name__ == '__main__':
    unittest.main()