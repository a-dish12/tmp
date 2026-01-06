"""Unit tests for the SurpriseMeForm."""
from django.test import TestCase
from django import forms

from recipes.forms.surprise_me_form import SurpriseMeForm
from recipes.constants.filters import MEAL_TYPES, TIME_FILTERS, DIET_FILTERS


class SurpriseMeFormTestCase(TestCase):
    """Unit tests for the SurpriseMeForm."""

    def test_form_has_expected_fields(self):
        form = SurpriseMeForm()
        self.assertIn('meal_type', form.fields)
        self.assertIn('time_filter', form.fields)
        self.assertIn('diet_filter', form.fields)

    def test_meal_type_field_is_optional_multiple_choice(self):
        field = SurpriseMeForm().fields['meal_type']
        self.assertIsInstance(field, forms.MultipleChoiceField)
        self.assertFalse(field.required)
        self.assertIsInstance(field.widget, forms.CheckboxSelectMultiple)

    def test_time_filter_field_is_optional_radio(self):
        field = SurpriseMeForm().fields['time_filter']
        self.assertIsInstance(field, forms.ChoiceField)
        self.assertFalse(field.required)
        self.assertIsInstance(field.widget, forms.RadioSelect)

    def test_diet_filter_field_is_required_radio(self):
        field = SurpriseMeForm().fields['diet_filter']
        self.assertIsInstance(field, forms.ChoiceField)
        self.assertTrue(field.required)
        self.assertIsInstance(field.widget, forms.RadioSelect)

    def test_form_valid_with_only_required_field(self):
        form = SurpriseMeForm(data={
            'diet_filter': DIET_FILTERS[0][0]
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_diet_filter(self):
        form = SurpriseMeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('diet_filter', form.errors)

    def test_form_accepts_all_fields(self):
        form = SurpriseMeForm(data={
            'meal_type': [MEAL_TYPES[0][0]],
            'time_filter': TIME_FILTERS[0][0],
            'diet_filter': DIET_FILTERS[0][0],
        })
        self.assertTrue(form.is_valid())
