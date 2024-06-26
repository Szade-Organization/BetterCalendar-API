import datetime
from urllib.parse import parse_qs, urlparse
import django
from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.management import call_command
from django.utils import timezone

from .models import *
from knox.models import AuthToken


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
    def setUp(self):
        self.user = User.objects.get(username='testuser')
        _token_instance, self.token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    @classmethod
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
    def setUp(self):
        self.user = User.objects.get(username='testuser')
        _token_instance, self.token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    @classmethod
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


class RegisterUserTestCase(APITestCase):
    def test_should_register_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_should_not_register_user_with_existing_username(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        _ = self.client.post('/api/auth/register/', data)
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0],
                         'A user with that username already exists.')

    def test_should_send_email_to_verify_registration(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        _ = self.client.post('/api/auth/register/', data)
        email_content = django.core.mail.outbox[0].body
        parsed_url = urlparse(email_content)
        query_params = parse_qs(parsed_url.query)

        verify_data = {
            "user_id": query_params.get('user_id', [None])[0],
            "timestamp": query_params.get('timestamp', [None])[0],
            "signature": query_params.get('signature', [None])[0]
        }

        response = self.client.post(
            '/api/auth/verify-registration/', verify_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'User verified successfully')
        self.assertTrue(User.objects.get(username='testuser').is_active)
        
        
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_should_not_verify_user_with_invalid_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        _ = self.client.post('/api/auth/register/', data)

        verify_data = {
            "user_id": User.objects.get(username='testuser').id,
            "timestamp": 1234124,
            "signature": "invalid_signature"
        }

        response = self.client.post(
            '/api/auth/verify-registration/', verify_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Invalid signature')
        self.assertFalse(User.objects.get(username='testuser').is_active)

    def test_should_change_password(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        _ = self.client.post('/api/auth/register/', data)
        email_content = django.core.mail.outbox[0].body
        parsed_url = urlparse(email_content)
        query_params = parse_qs(parsed_url.query)

        verify_data = {
            "user_id": query_params.get('user_id', [None])[0],
            "timestamp": query_params.get('timestamp', [None])[0],
            "signature": query_params.get('signature', [None])[0]
        }

        response = self.client.post(
            '/api/auth/verify-registration/', verify_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'User verified successfully')
        self.assertTrue(User.objects.get(username='testuser').is_active)

        change_password_data = {
            'login': 'testuser',
        }
        _ = self.client.post(
            '/api/auth/send-reset-password-link/', change_password_data)

        email_content = django.core.mail.outbox[1].body
        parsed_url = urlparse(email_content)
        query_params = parse_qs(parsed_url.query)

        change_password_data = {
            "user_id": query_params.get('user_id', [None])[0],
            "timestamp": query_params.get('timestamp', [None])[0],
            "signature": query_params.get('signature', [None])[0],
            "password": "newpassword123",
        }

        response = self.client.post(
            '/api/auth/reset-password/', change_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Reset password successful')

        login_data = {
            'username': 'testuser',
            'password': 'newpassword123'
        }

        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)


class UserActivityViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.get(username='testuser')
        _token_instance, self.token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser')
        cls.category = Category.objects.create(
            name='test_category', user=cls.user)
        cls.activity = Activity.objects.create(
            user=cls.user,
            category=cls.category,
            date_start=timezone.now() - timezone.timedelta(hours=1),
            date_end=timezone.now() + timezone.timedelta(hours=1)
        )
        cls.activity_recent = Activity.objects.create(
            user=cls.user,
            category=cls.category,
            date_start=timezone.now() - timezone.timedelta(days=1),
            date_end=timezone.now() - timezone.timedelta(hours=1)
        )
        cls.activity_next = Activity.objects.create(
            user=cls.user,
            category=cls.category,
            date_start=timezone.now() + timezone.timedelta(hours=1),
            date_end=timezone.now() + timezone.timedelta(days=1)
        )
        

    def test_fetch_all_current_activities(self):
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': [0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['current']), 1)
        self.assertEqual(response.data['current'][0]['id'], self.activity.id)
        
    def test_fetch_all_recent_activities(self):
        response = self.client.get('/api/get-activity/', {'state': ['recent'], 'count': [0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['recent']), 1)
        self.assertEqual(response.data['recent'][0]['id'], self.activity_recent.id)
        
    def test_fetch_all_next_activities(self):
        response = self.client.get('/api/get-activity/', {'state': ['next'], 'count': [0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['next']), 1)
        self.assertEqual(response.data['next'][0]['id'], self.activity_next.id)
        
    def test_fetch_all_activities(self):
        response = self.client.get('/api/get-activity/', {'state': ['current', 'recent', 'next'], 'count': [0, 0, 0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['current']), 1)
        self.assertEqual(response.data['current'][0]['id'], self.activity.id)
        self.assertEqual(len(response.data['recent']), 1)
        self.assertEqual(response.data['recent'][0]['id'], self.activity_recent.id)
        self.assertEqual(len(response.data['next']), 1)
        self.assertEqual(response.data['next'][0]['id'], self.activity_next.id)
        
    def test_fetch_multiple_current_activities(self):
        self.activity_current2 = Activity.objects.create(
            user=self.user,
            category=self.category,
            date_start=timezone.now() - timezone.timedelta(hours=0.5),
            date_end=timezone.now() + timezone.timedelta(hours=1)
        )
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': [1]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['current']), 1)
        self.assertEqual(response.data['current'][0]['id'], self.activity.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': [2]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['current']), 2)
        self.assertEqual(response.data['current'][0]['id'], self.activity.id)
        self.assertEqual(response.data['current'][1]['id'], self.activity_current2.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': [3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['current']), 2)
        self.assertEqual(response.data['current'][0]['id'], self.activity.id)
        self.assertEqual(response.data['current'][1]['id'], self.activity_current2.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': [0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['current']), 2)
        self.assertEqual(response.data['current'][0]['id'], self.activity.id)
        self.assertEqual(response.data['current'][1]['id'], self.activity_current2.id)
        
    def test_fetch_multiple_recent_activities(self):
        self.activity_recent2 = Activity.objects.create(
            user=self.user,
            category=self.category,
            date_start=timezone.now() - timezone.timedelta(days=2),
            date_end=timezone.now() - timezone.timedelta(days=1)
        )
        response = self.client.get('/api/get-activity/', {'state': ['recent'], 'count': [1]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['recent']), 1)
        self.assertEqual(response.data['recent'][0]['id'], self.activity_recent.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['recent'], 'count': [2]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['recent']), 2)
        self.assertEqual(response.data['recent'][0]['id'], self.activity_recent.id)
        self.assertEqual(response.data['recent'][1]['id'], self.activity_recent2.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['recent'], 'count': [3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['recent']), 2)
        self.assertEqual(response.data['recent'][0]['id'], self.activity_recent.id)
        self.assertEqual(response.data['recent'][1]['id'], self.activity_recent2.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['recent'], 'count': [0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['recent']), 2)
        self.assertEqual(response.data['recent'][0]['id'], self.activity_recent.id)
        self.assertEqual(response.data['recent'][1]['id'], self.activity_recent2.id)
        
    def test_fetch_multiple_next_activities(self):
        self.activity_next2 = Activity.objects.create(
            user=self.user,
            category=self.category,
            date_start=timezone.now() + timezone.timedelta(days=1),
            date_end=timezone.now() + timezone.timedelta(days=2)
        )
        response = self.client.get('/api/get-activity/', {'state': ['next'], 'count': [1]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['next']), 1)
        self.assertEqual(response.data['next'][0]['id'], self.activity_next.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['next'], 'count': [2]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['next']), 2)
        self.assertEqual(response.data['next'][0]['id'], self.activity_next.id)
        self.assertEqual(response.data['next'][1]['id'], self.activity_next2.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['next'], 'count': [3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['next']), 2)
        self.assertEqual(response.data['next'][0]['id'], self.activity_next.id)
        self.assertEqual(response.data['next'][1]['id'], self.activity_next2.id)
        
        response = self.client.get('/api/get-activity/', {'state': ['next'], 'count': [0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['next']), 2)
        self.assertEqual(response.data['next'][0]['id'], self.activity_next.id)
        self.assertEqual(response.data['next'][1]['id'], self.activity_next2.id)
        
    def test_wrong_arguments_provided(self):
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': []})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get('/api/get-activity/', {'state': [], 'count': [1]})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get('/api/get-activity/', {'state': ['current', 'recent'], 'count': [1]})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get('/api/get-activity/', {'state': ['wrong'], 'count': [1]})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get('/api/get-activity/', {'state': ['current'], 'count': [1, 2]})
        self.assertEqual(response.status_code, 400)
        