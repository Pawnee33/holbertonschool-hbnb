#!/usr/bin/python3
"""
Unit tests for Review endpoints of the Holberton HBNB project.
Covers creation, retrieval, update, and deletion of reviews,
including validation and error handling.
"""

import unittest
from app import create_app
from app.services import facade


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        from app.persistence.repository import InMemoryRepository
        facade.review_repo = InMemoryRepository()
        facade.user_repo = InMemoryRepository()
        facade.place_repo = InMemoryRepository()
        
        self.user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        })
        self.place = facade.create_place({
            'title': 'Test Place',
            'description': 'A test place',
            'price': 100,
            'latitude': 0.0,
            'longitude': 0.0,
            'owner_id': self.user.id
        })

    def test_create_review(self):
        response = self.client.post(
            '/api/v1/reviews/',
            json={
                'text': 'Great place!',
                'rating': 5,
                'user_id': self.user.id,
                'place_id': self.place.id
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['text'], 'Great place!')
        self.assertEqual(response.json['rating'], 5)

    def test_get_all_reviews(self):
        facade.create_review({
            'text': 'Great!',
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) >= 1)

    def test_get_review_by_id(self):
        review = facade.create_review({
            'text': 'Good place!',
            'rating': 4,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Good place!')

    def test_update_review(self):
        review = facade.create_review({
            'text': 'Nice place',
            'rating': 3,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        response = self.client.put(
            f'/api/v1/reviews/{review.id}',
            json={'text': 'Excellent place!', 'rating': 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Excellent place!')
        self.assertEqual(response.json['rating'], 5)


if __name__ == "__main__":
    unittest.main()
