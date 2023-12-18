from faker import Faker
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

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

    def handle(self, *args, **kwargs):
        users_desired = kwargs['users']
        categories_desired = kwargs['categories']
        activities_desired = kwargs['activities']
        users_count = User.objects.count()
        categories_count = Category.objects.count()
        activities_count = Activity.objects.count()

        if (users_desired is None and users_count == 0) and (categories_desired is not None or activities_desired is not None):
            raise Exception(
                'The users argument is empty and there are no users in the database. Please provide at least one user.')
        if (categories_desired is None and activities_desired is not None) and categories_count == 0:
            raise Exception(
                'The categories argument is empty and there are no categories in the database. Please provide at least one category.')

        fake = Faker()

        if users_desired is not None:
            users_to_create = users_desired - users_count
            if users_to_create > 0:
                for _ in range(users_to_create):
                    user_username = fake.user_name()
                    user_email = fake.email()
                    user_password = fake.password()
                    User.objects.create_user(
                        username=user_username,
                        email=user_email,
                        password=user_password
                    )
                    print(f'Created user {user_username}')
                print(f'Created {users_to_create} users.')
            elif users_to_create < 0:
                print("deleting")
                for _ in range(-users_to_create):
                    user = User.objects.all()[fake.random_int(
                        0, User.objects.count() - 1)]
                    user.delete()
                    print(f'Deleted user {user.username}')
                print(f'Deleted {-users_to_create} users.')

        if categories_desired is not None:
            categories_dict = {
                'studying': 'Engaging in learning activities in a specific subject or area.',
                'exercise': 'Physical activity done for the purpose of improving health and fitness.',
                'work': 'Tasks and activities related to professional or occupational responsibilities.',
                'meeting': 'Gathering of individuals for discussion or collaboration on a specific topic.',
                'socializing': 'Interacting with others for recreational or social purposes.',
                'personal': 'Tasks and activities related to personal well-being and interests.',
                'coding': 'Writing and debugging code for software development.',
                'reading': 'Spending time with written material to gain knowledge or enjoyment.',
                'writing': 'Creating written content, such as articles, stories, or blog posts.',
                'meditation': 'Practicing mindfulness and relaxation techniques for mental well-being.',
                'cooking': 'Preparing and cooking meals or recipes.',
                'gardening': 'Cultivating and tending to plants and gardens.',
                'volunteering': 'Contributing time and effort to a charitable cause or organization.',
                'music': 'Engaging in musical activities, such as playing instruments or listening to music.',
                'travel': 'Exploring new places and experiencing different cultures.',
                'hobbies': 'Pursuing personal interests and recreational activities.',
                'shopping': 'Purchasing goods and services for personal or household needs.',
                'self-care': 'Engaging in activities that promote physical and mental well-being.',
                'finance': 'Managing personal finances and budgeting.',
                'yoga': 'Practicing yoga for physical and mental health.'
            }
            categories_to_create = categories_desired - categories_count
            if categories_to_create > 0:
                for _ in range(categories_to_create):
                    category_name = list(categories_dict.keys())[
                        fake.random_int(0, len(categories_dict) - 1)]
                    category_user = User.objects.all(
                    )[fake.random_int(0, users_count - 1)]
                    category_description = categories_dict[category_name]
                    category_color = fake.color_name()
                    category_icon = fake.file_name(extension='svg')
                    category_importance_level = fake.random_element(
                        elements=('M', 'S', 'C', 'W', 'N'))
                    Category.objects.create(
                        name=category_name,
                        user=category_user,
                        description=category_description,
                        color=category_color,
                        icon=category_icon,
                        importance_level=category_importance_level
                    )
                    print(f'Created category {category_name}')
                print(f'Created {categories_to_create} categories.')
            elif categories_to_create < 0:
                for _ in range(-categories_to_create):
                    category = Category.objects.all()[fake.random_int(
                        0, Category.objects.count() - 1)]
                    category.delete()
                    print(f'Deleted category {category.name}')
                print(f'Deleted {-categories_to_create} categories.')

        if activities_desired is not None:
            activities_dict = {
                "Meeting with Andrew": "Meeting with Andrew Brown on Long Street.",
                "Gym workout": "Strength training and cardio exercises at the gym.",
                "Study group session": "Collaborative study session with classmates.",
                "Client call": "Scheduled call with a client to discuss project details.",
                "Lunch with friends": "Casual lunch outing with friends at a local restaurant.",
                "Personal project work": "Working on personal projects or hobbies.",
                "Team brainstorming": "Collaborative session to brainstorm ideas with the team.",
                "Networking event": "Attending an event to network with professionals in the industry.",
                "Family dinner": "Gathering with family for a shared meal at home.",
                "Movie night": "Watching a movie or TV series for entertainment.",
                "Volunteer work": "Participating in volunteer activities for a charitable cause.",
                "Coffee meeting": "Meeting someone for a casual coffee discussion.",
                "Home workout": "Exercising at home with bodyweight exercises or home gym equipment.",
                "Board game night": "Playing board games with friends or family.",
                "Webinar attendance": "Participating in an online webinar or virtual event.",
                "Writing blog post": "Creating content for a personal or professional blog.",
                "Grocery shopping": "Buying groceries and household essentials.",
                "Doctor's appointment": "Scheduled visit to the doctor for a health check-up.",
                "Photography session": "Engaging in photography and capturing images.",
                "Online course": "Taking an online course to learn new skills or enhance knowledge.",
                "Tech meetup": "Attending a technology-focused meetup or conference.",
                "Cooking class": "Participating in a cooking class to learn new recipes.",
                "Date night": "Planned evening with a significant other for a date.",
                "Podcast recording": "Recording and producing content for a personal or professional podcast.",
                "Home cleaning": "Cleaning and organizing the living space.",
                "Book club meeting": "Discussion meeting with a book club to talk about a selected book.",
                "Sprint planning": "Agile sprint planning session for project management.",
                "Art exhibition": "Visiting an art exhibition or gallery for cultural enrichment.",
                "Financial planning": "Reviewing and planning personal or business finances.",
                "Game development": "Working on the development of a video or board game.",
                "Social media management": "Managing and scheduling content for social media platforms.",
                "Language learning": "Dedicating time to learn a new language or improve language skills.",
                "Pet grooming": "Taking care of grooming needs for pets.",
                "Science fair preparation": "Preparing for participation in a science fair or exhibition.",
                "Home improvement": "Engaging in DIY home improvement projects.",
                "Camping trip": "Planning and preparing for a camping trip.",
                "Team building activity": "Participating in team-building exercises with colleagues.",
                "DIY craft project": "Creating handmade crafts or DIY projects.",
                "Job interview": "Attending a job interview for a potential employment opportunity.",
                "Tech support for family": "Assisting family members with technical issues or support.",
                "Salsa dance class": "Taking a dance class to learn salsa or other dance forms.",
                "Product launch preparation": "Preparing for the launch of a new product or service.",
                "Mindfulness meditation": "Practicing mindfulness meditation for mental well-being.",
                "Gardening session": "Tending to the garden and planting new flowers or vegetables.",
                "Home budgeting": "Reviewing and managing personal or household budget.",
                "Virtual reality gaming": "Engaging in gaming using virtual reality technology.",
                "Home office setup": "Organizing and setting up a productive home office space.",
                "Charity run": "Participating in a charity run or marathon event.",
                "Escape room experience": "Participating in an escape room challenge for entertainment.",
                "Online multiplayer gaming": "Playing video games online with friends or others.",
                "Podcast listening": "Listening to podcasts for entertainment or knowledge.",
                "Academic research": "Conducting research for academic or professional purposes.",
                "Home movie marathon": "Watching a series of movies at home in a single sitting.",
                "Cycling expedition": "Going on a cycling adventure or long-distance ride.",
                "Interior decorating": "Decorating and styling the interior of living spaces.",
                "Software update installations": "Updating software and applications on devices.",
                "Community cleanup": "Participating in a community cleanup or environmental initiative.",
                "Online shopping": "Browsing and purchasing items through online shopping platforms.",
                "Board game creation": "Designing and creating a new board game.",
                "Trivia night": "Participating in a trivia competition or quiz night.",
                "Online dating profile setup": "Creating or updating an online dating profile.",
                "Puzzle solving": "Engaging in solving puzzles for mental stimulation.",
                "Comic book reading": "Reading comic books or graphic novels for entertainment.",
                "Craft beer tasting": "Exploring and tasting different craft beers.",
                "Karaoke night": "Participating in karaoke singing at a local venue.",
                "Documentary watching": "Watching documentaries for educational or informative content.",
                "Running errands": "Completing various errands and tasks outside the home.",
                "Astrophotography": "Photographing celestial objects and astronomical events.",
                "Bike maintenance": "Performing maintenance on a bicycle.",
                "Online chess game": "Playing chess online with opponents.",
                "Parent-teacher meeting": "Meeting with teachers to discuss a child's academic progress.",
                "Dentist appointment": "Scheduled visit to the dentist for dental check-up and care.",
                "Personal finance review": "Reviewing personal financial goals and investments.",
                "DIY home spa day": "Creating a relaxing spa experience at home.",
                "Family board game night": "Playing board games with family members.",
                "Collectible card gaming": "Participating in collectible card games like Magic: The Gathering.",
                "Art and wine night": "Combining art activities with wine tasting for a creative experience.",
                "Virtual travel exploration": "Exploring virtual travel destinations through online platforms.",
                "Neighborhood clean-up": "Participating in a local neighborhood clean-up initiative.",
                "Ice cream tasting": "Sampling and trying different flavors of ice cream.",
                "Local museum visit": "Visiting a local museum for cultural and historical exploration.",
                "Candle making": "Creating handmade candles through a candle-making process.",
                "Virtual reality travel experience": "Exploring virtual reality travel simulations.",
                "Photobook creation": "Compiling and creating a photobook with memorable photos.",
                "Online cooking class": "Participating in a virtual cooking class to learn new recipes.",
                "Online board game night": "Playing board games with friends through online platforms.",
            }
            activities_to_create = activities_desired - activities_count
            if activities_to_create > 0:
                for _ in range(activities_to_create):
                    activity_name = list(activities_dict.keys())[
                        fake.random_int(0, len(activities_dict) - 1)]
                    activity_user = User.objects.all(
                    )[fake.random_int(0, users_count - 1)]
                    activity_category = Category.objects.all(
                    )[fake.random_int(0, categories_count - 1)]
                    activity_description = activities_dict[activity_name]
                    activity_date_start = make_aware(
                        fake.date_time_between(start_date='-1y', end_date='+1y'))
                    activity_date_end = make_aware(fake.date_time_between(
                        start_date=activity_date_start, end_date='+1y'))
                    activity_length = activity_date_end - activity_date_start
                    activity_is_planned = fake.boolean()
                    activity_importance_level = fake.random_element(
                        elements=('M', 'S', 'C', 'W', 'N'))
                    Activity.objects.create(
                        name=activity_name,
                        user=activity_user,
                        category=activity_category,
                        description=activity_description,
                        date_start=activity_date_start,
                        date_end=activity_date_end,
                        length=activity_length,
                        is_planned=activity_is_planned,
                        importance_level=activity_importance_level
                    )
                    print(f'Created activity {activity_name}')
                print(f'Created {activities_to_create} activities.')
            elif activities_to_create < 0:
                for _ in range(-activities_to_create):
                    activity = Activity.objects.all()[fake.random_int(
                        0, Activity.objects.count() - 1)]
                    activity.delete()
                    print(f'Deleted activity {activity.name}')
                print(f'Deleted {-activities_to_create} activities.')

        print('Generating fake data completed.')
        print('User count: ' + str(User.objects.count()))
        print('Category count: ' + str(Category.objects.count()))
        print('Activity count: ' + str(Activity.objects.count()))
