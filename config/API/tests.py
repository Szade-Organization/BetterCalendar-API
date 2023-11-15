from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.
class APIInformationViewTestCase(APITestCase):    
    def test_should_return_404_for_invalid_url(self):
        response = self.client.get('/api/invalid')
        self.assertEqual(response.status_code, 404)
        
    def test_get_correct_data(self):
        response = self.client.get('/api/info')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['api_name'], 'BetterCalendar-API')
