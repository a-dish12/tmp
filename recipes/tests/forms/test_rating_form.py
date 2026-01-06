"""Unit tests for the RatingForm."""
from django.test import TestCase
from django import forms

from recipes.forms.rating_form import RatingForm
from recipes.models import User, Recipe, Rating


class RatingFormTestCase(TestCase):
    """Unit tests for the RatingForm."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')

        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Flour",
            time=20,
            meal_type="lunch"
        )

        self.valid_input = {
            'stars': 4
        }

    # ---------- Field checks ----------

    def test_form_has_stars_field(self):
        form = RatingForm()
        self.assertIn('stars', form.fields)

    def test_stars_field_is_choice_field(self):
        form = RatingForm()
        self.assertIsInstance(form.fields['stars'], forms.ChoiceField)

    def test_stars_field_uses_radio_select(self):
        form = RatingForm()
        self.assertIsInstance(form.fields['stars'].widget, forms.RadioSelect)

    # ---------- Validation ----------

    def test_form_accepts_valid_rating(self):
        form = RatingForm(data=self.valid_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_rating_below_1(self):
        form = RatingForm(data={'stars': 0})
        self.assertFalse(form.is_valid())

    def test_form_rejects_rating_above_5(self):
        form = RatingForm(data={'stars': 6})
        self.assertFalse(form.is_valid())

    def test_form_rejects_missing_rating(self):
        form = RatingForm(data={})
        self.assertFalse(form.is_valid())

    # ---------- Saving ----------

    def test_form_saves_rating_correctly(self):
        form = RatingForm(data=self.valid_input)
        self.assertTrue(form.is_valid())

        rating = form.save(commit=False)
        rating.user = self.user
        rating.recipe = self.recipe
        rating.save()

        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(rating.stars, 4)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.recipe, self.recipe)
