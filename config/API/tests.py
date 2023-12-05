from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *

# Create your tests here.
class APIInformationViewTestCase(APITestCase):    
    def test_should_return_404_for_invalid_url(self):
        response = self.client.get('/api/invalid')
        self.assertEqual(response.status_code, 404)
        
    def test_get_correct_status_code(self):
        response = self.client.get('/api/info')
        self.assertEqual(response.status_code, 200)    
    
    def test_get_correct_data(self):
        response = self.client.get('/api/info')
        self.assertEqual(response.data['api_name'], 'BetterCalendar-API')


class CategoryViewSetTestCase(APITestCase):
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser')
        cls.category = Category.objects.create(name='test_category', user=cls.user)
        
    def test_should_list_categories(self):
        response = self.client.get('/api/category/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)
        self.assertEqual(response.data[0]['user'], self.category.user.id)
        
    def test_should_create_category(self):
        data = {'name': 'test_category', 'user': self.user.id}
        response = self.client.post('/api/category/', data)
        self.assertEqual(response.status_code, 201)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])
            
    def test_should_retrieve_category(self):
        response = self.client.get(f'/api/category/{self.category.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.category.name)
        self.assertEqual(response.data['user'], self.category.user.id)
        
    def test_should_update_category(self):
        data = {'name': 'test_category_updated', 'user': self.user.id}
        response = self.client.put(f'/api/category/{self.category.id}/', data)
        self.assertEqual(response.status_code, 200)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])
    
    def test_should_partial_update_category(self):
        data = {'name': 'test_category_updated'}
        response = self.client.patch(f'/api/category/{self.category.id}/', data)
        self.assertEqual(response.status_code, 200)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])
            
    def test_should_destroy_category(self):
        response = self.client.delete(f'/api/category/{self.category.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
        

class ActivityViewSetTestCase(APITestCase):
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser')
        cls.category = Category.objects.create(name='test_category', user=cls.user)
        cls.activity = Activity.objects.create(name='test_activity', user=cls.user, category=cls.category)
    
    def test_should_list_activities(self):
        response = self.client.get('/api/activity/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.activity.name)
        self.assertEqual(response.data[0]['user'], self.activity.user.id)
        self.assertEqual(response.data[0]['category'], self.activity.category.id)
        
    def test_should_create_activity(self):
        data = {'name': 'test_activity', 'user': self.user.id, 'category': self.category.id}
        response = self.client.post('/api/activity/', data)
        self.assertEqual(response.status_code, 201) 
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])
    
    def test_should_retrieve_activity(self):
        response = self.client.get(f'/api/activity/{self.activity.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.activity.name)
        self.assertEqual(response.data['user'], self.activity.user.id)
        self.assertEqual(response.data['category'], self.activity.category.id)
        
    def test_should_update_activity(self):
        data = {'name': 'test_activity_updated', 'user': self.user.id, 'category': self.category.id}
        response = self.client.put(f'/api/activity/{self.activity.id}/', data)
        self.assertEqual(response.status_code, 200)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])
    
    def test_should_partial_update_activity(self):
        data = {'name': 'test_activity_updated'}
        response = self.client.patch(f'/api/activity/{self.activity.id}/', data)
        self.assertEqual(response.status_code, 200)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])
            
    def test_should_destroy_activity(self):
        response = self.client.delete(f'/api/activity/{self.activity.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Activity.objects.filter(id=self.activity.id).exists())