"""
Management command to seed the database with demo data.

This command creates a small set of named fixture users and then fills up
to ``USER_COUNT`` total users using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""


from faker import Faker
from faker_food import FoodProvider
import random
from django.core.management.base import BaseCommand, CommandError
from recipes.models import User, Recipe, Follow, Rating
from recipes.management import Recipe_Fixtures


user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

recipe_fixtures = Recipe_Fixtures.get_recipe_fixtures()

follow_fixtures = [
    {'follower': User.objects.get(id=1), 'following': User.objects.get(id=2)},
    {'follower': User.objects.get(id=1), 'following': User.objects.get(id=3)},
    {'follower': User.objects.get(id=2), 'following': User.objects.get(id=3)},
    {'follower': User.objects.get(id=3), 'following': User.objects.get(id=1)},
    {'follower': User.objects.get(id=3), 'following': User.objects.get(id=2)}
]

class Command(BaseCommand):
    """
    Build automation command to seed the database with data.

    This command inserts a small set of known users (``user_fixtures``) and then
    repeatedly generates additional random users until ``USER_COUNT`` total users
    exist in the database. Each generated user receives the same default password.

    It then inserts a larger set of known recipes (``recipe_fixtures``) and then
    repeatedly generates additional random recipes until ``RECIPE_COUNT`` total recipes
    exist in the database.
    The command also inserts a small set of known follow relations (``follow_fixtures``) and then
    repeatedly generates additional random follows until ``FOLLOW_COUNT`` total follow relations
    exist in the database.

    Attributes:
        USER_COUNT (int): Target total number of users in the database.
        RECIPE_COUNT (int): Target total number of recipes in the database.
        FOLLOW_COUNT (int): Target total number of follow relations in the database.
        RATING_COUNT (int): Target total number of ratings in the database.
        DEFAULT_PASSWORD (str): Default password assigned to all created users.
        help (str): Short description shown in ``manage.py help``.
        faker (Faker): Locale-specific Faker instance used for random data.
    """
    
    USER_COUNT = 200
    RECIPE_COUNT = 150
    FOLLOW_COUNT = 350
    RATING_COUNT = 1000

    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker('en_GB')
        self.faker.add_provider(FoodProvider)

    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores ``self.users``, ``self.recipes`` and ``self.follows``
        for any post-processing or debugging (not required for operation).
        """
        self.create_users()
        self.users = User.objects.all()
        self.create_recipes()
        self.recipes = Recipe.objects.all()

        self.create_follows()
        self.follows = Follow.objects.all()
        self.generate_random_ratings()


    #USERS

    def create_users(self):
        """
        Create fixture users and then generate random users up to USER_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on username/email) are ignored and generation continues.
        """
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        """Attempt to create each predefined fixture user."""
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        """
        Generate random users until the database contains USER_COUNT users.

        Prints a simple progress indicator to stdout during generation.
        """
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        """
        Generate a single random user and attempt to insert it.

        Uses Faker for first/last names, then derives a simple username/email.
        """
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_user(self, data):
        """
        Attempt to create a user and ignore any errors.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        """
        Create a user with the default password.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )


    #RECIPES

    def create_recipes(self):
        """
        Create fixture users and then generate random recipes up to RECIPE_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on username/email) are ignored and generation continues.
        """
        self.generate_recipe_fixtures()
        self.generate_random_recipes()

    def generate_recipe_fixtures(self):
        """Attempt to create each predefined fixture recipe."""
        for data in recipe_fixtures:
            self.try_create_recipe(data)

    def generate_random_recipes(self):
        """
        Generate random recipes until the database contains RECIPE_COUNT recipes.

        Prints a simple progress indicator to stdout during generation.
        """
        recipe_count = Recipe.objects.count()
        while  recipe_count < self.RECIPE_COUNT:
            print(f"Seeding recipe {recipe_count}/{self.RECIPE_COUNT}", end='\r')
            self.generate_recipe()
            recipe_count = Recipe.objects.count()
        print("Recipe seeding complete.      ")

    def generate_recipe(self):
        """
        Generate a single random recipe and attempt to insert it.

        Uses Faker for everything but meal_type, which is a random choice between options.
        """
        title = self.faker.dish()
        description = shorten_string(self.faker.dish_description())
        ingredients = f'{self.faker.ingredient()}\n{self.faker.ingredient()}'
        time = round_to_nearest_5(self.faker.random_int(min=5, max=150))
        meal_type = random.choice(['breakfast','lunch','dinner','snack','dessert'])
        self.try_create_recipe({'title': title, 'description': description, 'ingredients': ingredients,
         'time': time, 'meal_type': meal_type})

    def try_create_recipe(self, data):
        """
        Attempt to create a recipe and ignore any errors.

        Args:
            data (dict): Mapping with keys ``title``, ``description``,
                ``ingredients``, ``time``, and ``meal_type``.
        """
        try:
            self.create_recipe(data)
        except:
            pass

    def create_recipe(self, data):
        """
        Create a recipe.

        Args:
            data (dict): Mapping with keys ``title``, ``description``,
                ``ingredients``, ``time``, and ``meal_type``.
        """
        Recipe.objects.create(
            author=random.choice(self.users),
            title=data['title'],
            description=data['description'],
            ingredients=data['ingredients'],
            time=data['time'],
            meal_type=data['meal_type'],
        )


    #FOLLOW

    def create_follows(self):
        """
        Create fixture follow relationships and then generate random follows up to FOLLOW_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on the follow relation) are ignored and generation continues.
        """
        self.generate_follow_fixtures()
        self.generate_random_follows()

    def generate_follow_fixtures(self):
        """Attempt to create each predefined fixture follow."""
        for data in follow_fixtures:
            self.try_create_follow(data)

    def generate_random_follows(self):
        """
        Generate random follows until the database contains FOLLOW_COUNT follow relations.

        Prints a simple progress indicator to stdout during generation.
        """
        follow_count = Follow.objects.count()
        while follow_count < self.FOLLOW_COUNT:
            print(f"Seeding follow {follow_count}/{self.FOLLOW_COUNT}", end='\r')
            self.generate_follow()
            follow_count = Follow.objects.count()
        print("Follow seeding complete.      ")

    def generate_follow(self):
        """
        Generate a single random follow relation and attempt to insert it.
        """
        this_user = random.choice(self.users)
        follower = this_user
        following = random.choice(self.users.exclude(id=this_user.id))
        self.try_create_follow({'follower': follower, 'following': following})

    def try_create_follow(self, data):
        """
        Attempt to create a follow and ignore any errors.

        Args:
            data (dict): Mapping with keys ``follower`` and ``following``
        """
        try:
            self.create_follow(data)
        except:
            pass

    def create_follow(self, data):
        """
        Creates follow relation if it doesn't already exist.

        Args:
            data (dict): Mapping with keys ``follower`` and ``following``
        """
        Follow.objects.get_or_create(
            follower=data['follower'],
            following=data['following']
        )


    #RATING

    def generate_random_ratings(self):
        """
        Generate random ratings until the database contains RATING_COUNT ratings.

        Prints a simple progress indicator to stdout during generation.
        """
        rating_count = Rating.objects.count()
        while rating_count < self.RATING_COUNT:
            print(f"Seeding rating {rating_count}/{self.RATING_COUNT}", end='\r')
            self.generate_rating()
            rating_count = Rating.objects.count()
        print("Rating seeding complete.      ")

    def generate_rating(self):
        """
        Generate a single random rating and attempt to insert it.
        """
        recipe = random.choice(self.recipes)
        user = random.choice(self.users)
        stars = random.choice([1, 2, 3, 4, 5])
        self.try_create_rating({'recipe': recipe, 'user': user, 'stars': stars})

    def try_create_rating(self, data):
        """
        Attempt to create a rating and ignore any errors.

        Args:
            data (dict): Mapping with keys ``recipe``, ``user`` and ``stars``
        """
        try:
            self.create_rating(data)
        except:
            pass

    def create_rating(self, data):
        """
        Creates rating if it doesn't already exist.

        Args:
            data (dict): Mapping with keys ``recipe``, ``user`` and ``stars``
        """
        Rating.objects.create(
            recipe=data['recipe'],
            user=data['user'],
            stars=data['stars']
        )


def create_username(first_name, last_name):
        """
        Construct a simple username from first and last names.

        Args:
            first_name (str): Given name.
            last_name (str): Family name.

        Returns:
            str: A username in the form ``@{firstname}{lastname}`` (lowercased).
        """
        return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
        """
        Construct a simple example email address.

        Args:
            first_name (str): Given name.
            last_name (str): Family name.

        Returns:
            str: An email in the form ``{firstname}.{lastname}@example.org``.
        """
        return first_name + '.' + last_name + '@example.org'

def round_to_nearest_5(num):
        """
        Rounds the given integer to the nearest 5.
        """
        return 5 * round(num/5)

def shorten_string(s):
        """
        Cuts the given string to a reasonable length.
        """
        s = s.split('.')[0]
        if len(s) <= 110:
            return s + '.'
        else:
            s = s.split(',')[0]
            if '(' in s and ')' not in s:
                return s +').'
            else:
                return s + '.'