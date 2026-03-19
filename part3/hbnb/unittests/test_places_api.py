#!/usr/bin/python3

import unittest
import uuid
from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        facade.user_repo.clear()
        facade.place_repo.clear()
        facade.review_repo.clear()
        facade.amenity_repo.clear()

    def create_test_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john{uuid.uuid4()}@example.com"
        })
        self.assertEqual(response.status_code, 201)
        return response.get_json()["id"]

    def create_place_payload(
        self,
        owner_id,
        latitude=45,
        longitude=3,
        price=100
    ):
        return {
            "title": "Test Place",
            "description": "Nice place",
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "owner_id": owner_id,
            "amenities": []
        }

    def test_create_place_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id)
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Test Place")
        self.assertEqual(data["owner_id"], owner_id)

    def test_create_place_invalid_owner(self):
        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload("invalid-owner-id")
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


    def test_create_place_latitude_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, latitude=100)
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_place_latitude_positive_boundary_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, latitude=90)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_latitude_above_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, latitude=90.0001)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_latitude_negative_boundary_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, latitude=-90)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_latitude_below_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, latitude=-90.0001)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, longitude=300)
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_place_longitude_positive_boundary_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, longitude=180)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_longitude_above_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, longitude=180.0001)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_negative_boundary_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, longitude=-180)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_longitude_below_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, longitude=-180.0001)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_price_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, price=100)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_price_positive_boundary_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, price=0.5)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_price_zero_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, price=0)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_price_negative_boundary_valid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, price=-0.50)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_price_below_boundary_invalid(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, price=-180)
        )

        self.assertEqual(response.status_code, 400)

    def test_get_place_by_id_valid(self):
        owner_id = self.create_test_user()

        create_response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id)
        )
        self.assertEqual(create_response.status_code, 201)

        place_data = create_response.get_json()
        place_id = place_data["id"]

        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)

        data = get_response.get_json()

        self.assertEqual(data["id"], place_id)
        self.assertEqual(data["title"], "Test Place")
        self.assertEqual(data["owner"]["id"], owner_id)

    def test_get_place_by_id_not_found(self):
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn("error", data)

    def test_get_all_places(self):
        owner_id = self.create_test_user()

        create_response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id)
        )
        self.assertEqual(create_response.status_code, 201)

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        first_place = data[0]
        self.assertIn("id", first_place)
        self.assertIn("title", first_place)
        self.assertIn("latitude", first_place)
        self.assertIn("longitude", first_place)

    def test_get_all_places_empty(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data, [])

    def test_update_place_valid(self):
        owner_id = self.create_test_user()

        create_response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id)
        )
        place_id = create_response.get_json()["id"]

        update_response = self.client.put(
            f'/api/v1/places/{place_id}',
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "price": 200,
                "latitude": 40,
                "longitude": 2,
                "owner_id": owner_id,
                "amenities": []
            }
        )

        self.assertEqual(update_response.status_code, 200)

        data = update_response.get_json()
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["price"], 200)

    def test_update_place_not_found(self):
        response = self.client.put(
            '/api/v1/places/nonexistent-id',
            json={}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_update_place_cannot_change_owner(self):
        owner_id = self.create_test_user()

        create_response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id)
        )
        place_id = create_response.get_json()["id"]

        response = self.client.put(
            f'/api/v1/places/{place_id}',
            json=self.create_place_payload(owner_id)
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["owner_id"], owner_id)

    def test_create_place_missing_title(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json={
                "description": "Nice place",
                "price": 100,
                "latitude": 45,
                "longitude": 3,
                "owner_id": owner_id,
                "amenities": []
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_price_type(self):
        owner_id = self.create_test_user()

        response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id, price="abc")
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_title_too_long(self):
        owner_id = self.create_test_user()
        long_title = "A" * 101

        payload = self.create_place_payload(owner_id)
        payload["title"] = long_title

        response = self.client.post('/api/v1/places/', json=payload)

        self.assertEqual(response.status_code, 400)

    def test_update_place_invalid_price(self):
        owner_id = self.create_test_user()

        create_response = self.client.post(
            '/api/v1/places/',
            json=self.create_place_payload(owner_id)
        )
        place_id = create_response.get_json()["id"]

        response = self.client.put(
            f'/api/v1/places/{place_id}',
            json=self.create_place_payload(owner_id, price=-10)
        )

        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()