import datetime
from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.management import call_command

from .models import *


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
        cls.category = Category.objects.create(
            name='test_category', user=cls.user)

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
        response = self.client.patch(
            f'/api/category/{self.category.id}/', data)
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
        cls.category = Category.objects.create(
            name='test_category', user=cls.user)
        cls.activity = Activity.objects.create(
            name='test_activity', user=cls.user, category=cls.category)
        cls.category2 = Category.objects.create(
            name='test_category2', user=cls.user)
        cls.activity2 = Activity.objects.create(
            name='test_activity2', user=cls.user, category=cls.category2,
            date_start=datetime.datetime(
                2021, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            date_end=datetime.datetime(2021, 1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))

    def test_should_list_activities(self):
        response = self.client.get('/api/activity/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        for a in response.data:
            if a['id'] == self.activity.id:
                self.assertEqual(a['name'], self.activity.name)
                self.assertEqual(a['user'], self.activity.user.id)
                self.assertEqual(a['category'], self.activity.category.id)
                break
        else:
            self.fail('activity not found')

    def test_should_list_activities_with_certain_category(self):
        response = self.client.get(
            f'/api/activity/', data={'category': self.category2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.activity2.name)
        self.assertEqual(response.data[0]['user'], self.activity2.user.id)
        self.assertEqual(
            response.data[0]['category'], self.activity2.category.id)

    def test_should_list_activities_with_is_planned_param(self):
        response = self.client.get(
            f'/api/activity/', data={'is_planned': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.activity2.id)

    def test_should_create_activity(self):
        data = {'name': 'test_activity', 'user': self.user.id,
                'category': self.category.id}
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
        data = {'name': 'test_activity_updated',
                'user': self.user.id, 'category': self.category.id}
        response = self.client.put(f'/api/activity/{self.activity.id}/', data)
        self.assertEqual(response.status_code, 200)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])

    def test_should_partial_update_activity(self):
        data = {'name': 'test_activity_updated'}
        response = self.client.patch(
            f'/api/activity/{self.activity.id}/', data)
        self.assertEqual(response.status_code, 200)
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])

    def test_should_destroy_activity(self):
        response = self.client.delete(f'/api/activity/{self.activity.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Activity.objects.filter(id=self.activity.id).exists())

    def test_should_be_planned_if_date_specified(self):
        data = {
            'name': 'test_activity_updated',
            'user': self.user.id,
            'category': self.category.id,
            'date_start': '2021-01-01T00:00:00Z',
            'date_end': '2021-01-01T01:00:00Z'
        }
        response = self.client.post('/api/activity/', data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['is_planned'])

    def test_should_not_be_planned_if_date_not_specified(self):
        response = self.client.get(f'/api/activity/{self.activity.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_planned'])

    def test_should_raise_validation_error_if_date_is_invalid(self):
        data = {
            'name': 'activity with invalid date',
            'user': self.user.id,
            'category': self.category.id,
            'date_start': datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            'date_end': datetime.datetime(2011, 1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        }
        response = self.client.post('/api/activity/', data)
        self.assertEqual(response.status_code, 400)