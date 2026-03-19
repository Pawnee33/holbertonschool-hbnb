#!/usr/bin/python3

import unittest
import uuid
from app import create_app
from app.services import facade


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        facade.user_repo.clear()
        facade.place_repo.clear()
        facade.review_repo.clear()
        facade.amenity_repo.clear()

    def create_user_payload(self, first_name="John", last_name="Doe", email=None):
        if email is None:
            email = f"john{uuid.uuid4()}@example.com"
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }

    def test_create_user_valid(self):
        response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload()
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")

    def test_create_user_missing_first_name(self):
        payload = self.create_user_payload()
        payload.pop("first_name")

        response = self.client.post('/api/v1/users/', json=payload)

        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_last_name(self):
        payload = self.create_user_payload()
        payload.pop("last_name")

        response = self.client.post('/api/v1/users/', json=payload)

        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_email(self):
        payload = self.create_user_payload()
        payload.pop("email")

        response = self.client.post('/api/v1/users/', json=payload)

        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_format(self):
        payload = self.create_user_payload(email="invalid-email")

        response = self.client.post('/api/v1/users/', json=payload)

        self.assertEqual(response.status_code, 400)

    def test_create_user_email_already_registered(self):
        email = f"john{uuid.uuid4()}@example.com"

        self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload(email=email)
        )

        response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload(email=email)
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_user_first_name_boundary_valid(self):
        long_name = "A" * 50
        response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload(first_name=long_name)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_user_first_name_too_long(self):
        long_name = "A" * 51
        response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload(first_name=long_name)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_user_last_name_boundary_valid(self):
        long_name = "B" * 50
        response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload(last_name=long_name)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_user_last_name_too_long(self):
        long_name = "B" * 51
        response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload(last_name=long_name)
        )

        self.assertEqual(response.status_code, 400)

    def test_get_user_by_id_valid(self):
        create_response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload()
        )
        user_id = create_response.get_json()["id"]

        response = self.client.get(f'/api/v1/users/{user_id}')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["id"], user_id)

    def test_get_user_by_id_not_found(self):
        response = self.client.get('/api/v1/users/nonexistent-id')

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_get_all_users_empty(self):
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_all_users_with_data(self):
        self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload()
        )

        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_update_user_valid(self):
        create_response = self.client.post(
            '/api/v1/users/',
            json=self.create_user_payload()
        )
        user_id = create_response.get_json()["id"]

        response = self.client.put(
            f'/api/v1/users/{user_id}',
            json={
                "first_name": "Updated",
                "last_name": "Name",
                "email": f"updated{uuid.uuid4()}@example.com"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["first_name"], "Updated")

    def test_update_user_not_found(self):
        response = self.client.put(
            '/api/v1/users/nonexistent-id',
            json=self.create_user_payload()
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())


if __name__ == '__main__':
    unittest.main()