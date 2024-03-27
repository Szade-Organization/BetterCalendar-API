from datetime import timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.db import transaction

from API.models import *


class Command(BaseCommand):
    """
    This command generates or deletes fake data for the API.
    If the specified number of model is greater than the number of existing models, the command creates new models.
    If the specified number of model is less than the number of existing models, the command deletes existing models.
    Arguments:
    -u, --users: Number of users to create.
    -c, --categories: Number of categories to create.
    -a, --activities: Number of activities to create.
    --verbose: Verbosity on or off.
    Usage:
    python manage.py populate -u 10 -c 5 -a 100
    """

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int,
                            help='Number of users to create.')
        parser.add_argument('-c', '--categories', type=int,
                            help='Number of categories to create.')
        parser.add_argument('-a', '--activities', type=int,
                            help='Number of activities to create.')
        parser.add_argument('--verbose', action='store_true', 
                            help='Verbosity on or off.')

    def handle(self, *args, **kwargs):
        users_desired = kwargs['users']
        categories_desired = kwargs['categories']
        activities_desired = kwargs['activities']
        verbosity = kwargs['verbose']

        if ((users_desired is None and User.objects.count() == 0) and (categories_desired is not None or activities_desired is not None)) or (users_desired == 0 and (categories_desired is not None or activities_desired is not None)):
            raise Exception(
                'The users argument is empty and there are no users in the database. Please provide at least one user.')
        if ((categories_desired is None and activities_desired is not None) and Category.objects.count() == 0) or (categories_desired == 0 and activities_desired is not None):
            raise Exception(
                'The categories argument is empty and there are no categories in the database. Please provide at least one category.')

        fake = Faker()

        self.generate_fake_data(
            users_desired, categories_desired, activities_desired, verbosity, fake)
        print('Generating fake data completed.')
        print('User count: ' + str(User.objects.count()))
        print('Category count: ' + str(Category.objects.count()))
        print('Activity count: ' + str(Activity.objects.count()))

    def make_users(self, users_desired, verbosity, fake):
        def _create_user():
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
            return user

        def _delete_user():
            user = User.objects.all()[fake.random_int(
                0, User.objects.count() - 1)]
            user.delete()
            return user

        if users_desired is not None:
            users_to_create = users_desired - User.objects.count()
            users_before = User.objects.count()
            if users_to_create > 0:
                # creating users
                for _ in range(users_to_create):
                    name = _create_user().username
                    if verbosity:
                        print(f'Created user {name}')

            elif users_to_create < 0:
                # deleting users
                for _ in range(-users_to_create):
                    name = _delete_user().username
                    if verbosity:
                        print(f'Deleted user {name}')

            users_after = User.objects.count()
            if users_after > users_before:
                print(f'Created {users_after - users_before} users.')
            elif users_after < users_before:
                print(f'Deleted {users_before - users_after} users.')
            else:
                print(
                    'No users created or deleted as the desired number of users is equal to the number of existing users.')

    def make_categories(self, categories_desired, verbosity, fake):
        from .faker_data import categories_dict

        def _create_category():
            category_name = list(categories_dict.keys())[
                fake.random_int(0, len(categories_dict) - 1)]
            category_user = User.objects.all(
            )[fake.random_int(0, User.objects.count() - 1)]
            category_description = categories_dict[category_name]
            category_color = fake.color_name()
            category_icon = fake.file_name(extension='svg')
            category_importance_level = fake.random_element(
                elements=('M', 'S', 'C', 'W', 'N'))
            category = Category.objects.create(
                name=category_name,
                user=category_user,
                description=category_description,
                color=category_color,
                icon=category_icon,
                importance_level=category_importance_level
            )
            return category

        def _delete_category():
            if Category.objects.count() > 1:
                category = Category.objects.all()[fake.random_int(
                    0, Category.objects.count() - 1)]
            else:
                category = Category.objects.all()[0]
            category.delete()
            return category

        categories_to_create = categories_desired - Category.objects.count()
        categories_before = Category.objects.count()
        if categories_to_create > 0:
            for _ in range(categories_to_create):
                name = _create_category().name
                if verbosity:
                    print(f'Created category {name}')

        elif categories_to_create < 0:
            for _ in range(-categories_to_create):
                name = _delete_category().name
                if verbosity:
                    print(f'Deleted category {name}')

        categories_after = Category.objects.count()
        if categories_after > categories_before:
            print(
                f'Created {categories_after - categories_before} categories.')
        elif categories_after < categories_before:
            print(
                f'Deleted {categories_before - categories_after} categories.')
        else:
            print('No categories created or deleted as the desired number of categories is equal to the number of existing categories.')

    def make_activities(self, activities_desired, verbosity, fake):
        from .faker_data import activities_dict

        def _create_activity():
            activity_name = list(activities_dict.keys())[
                fake.random_int(0, len(activities_dict) - 1)]
            activity_user = User.objects.all(
            )[fake.random_int(0, User.objects.count() - 1)]
            activity_category = Category.objects.all(
            )[fake.random_int(0, Category.objects.count() - 1)]
            activity_description = activities_dict[activity_name]
            activity_date_start = make_aware(
                fake.date_time_between(start_date='-1y', end_date='+1y'))
            activity_date_end = make_aware(fake.date_time_between(
                start_date=activity_date_start, end_date=activity_date_start + timedelta(hours=6)))
            activity_length = activity_date_end - activity_date_start
            activity_importance_level = fake.random_element(
                elements=('M', 'S', 'C', 'W', 'N'))
            activity = Activity.objects.create(
                name=activity_name,
                user=activity_user,
                category=activity_category,
                description=activity_description,
                date_start=activity_date_start,
                date_end=activity_date_end,
                length=activity_length,
                importance_level=activity_importance_level
            )
            return activity

        def _delete_activity():
            if Activity.objects.count() > 1:
                activity = Activity.objects.all()[fake.random_int(
                    0, Activity.objects.count() - 1)]
            else:
                activity = Activity.objects.all()[0]
            activity.delete()
            return activity

        activities_to_create = activities_desired - Activity.objects.count()
        activities_before = Activity.objects.count()
        if activities_to_create > 0:
            for _ in range(activities_to_create):
                name = _create_activity().name
                if verbosity:
                    print(f'Created activity {name}')
        elif activities_to_create < 0:
            for _ in range(-activities_to_create):
                name = _delete_activity().name
                if verbosity:
                    print(f'Deleted activity {name}')

        activities_after = Activity.objects.count()
        if activities_after > activities_before:
            print(
                f'Created {activities_after - activities_before} activities.')
        elif activities_after < activities_before:
            print(
                f'Deleted {activities_before - activities_after} activities.')
        else:
            print('No activities created or deleted as the desired number of activities is equal to the number of existing activities.')

    def generate_fake_data(self, users_desired, categories_desired, activities_desired, verbosity, fake):
        if users_desired is not None:
            try:
                self.make_users(users_desired, verbosity, fake)
            except Exception as e:
                raise e

        if categories_desired is not None:
            try:
                self.make_categories(categories_desired, verbosity, fake)
            except Exception as e:
                raise e

        if activities_desired is not None:
            self.make_activities(activities_desired, verbosity, fake)
