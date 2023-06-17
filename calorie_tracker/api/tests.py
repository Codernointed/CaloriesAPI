
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Entry
from django.urls import reverse


class EntryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            role='regular',
            expected_calories=2000  
        )
        self.client.force_authenticate(user=self.user)

    def test_create_entry(self):
        response = self.client.post('/entries/', {
            'user': self.user.id,
            'date': '2023-06-12',
            'time': '10:00',
            'text': 'Breakfast',
            'calories': 300,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Entry.objects.count(), 1)


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'role': 'regular',
            'expected_calories': 2000  
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 1)
