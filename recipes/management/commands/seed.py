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
from recipes.models import User, Recipe
from recipes.management import Recipe_Fixtures


user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

recipe_fixtures = Recipe_Fixtures.get_recipe_fixtures()

class Command(BaseCommand):
    """
    Build automation command to seed the database with data.

    This command inserts a small set of known users (``user_fixtures``) and then
    repeatedly generates additional random users until ``USER_COUNT`` total users
    exist in the database. Each generated user receives the same default password.

    Attributes:
        USER_COUNT (int): Target total number of users in the database.
        RECIPE_COUNT (int): Target total number of recipes in the database.
        DEFAULT_PASSWORD (str): Default password assigned to all created users.
        help (str): Short description shown in ``manage.py help``.
        faker (Faker): Locale-specific Faker instance used for random data.
    """

    USER_COUNT = 200
    RECIPE_COUNT = 150
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

        Runs the full seeding workflow and stores ``self.users`` and ``self.recipes`` for any
        post-processing or debugging (not required for operation).
        """
        self.create_users()
        self.create_recipes()
        self.users = User.objects.all()
        self.recipes = Recipe.objects.all()


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
            author=random.choice(User.objects.all()),
            title=data['title'],
            description=data['description'],
            ingredients=data['ingredients'],
            time=data['time'],
            meal_type=data['meal_type'],
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
