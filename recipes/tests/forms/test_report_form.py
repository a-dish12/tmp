"""Unit tests for the ReportForm."""

from django.test import TestCase
from recipes.forms.report_form import ReportForm


class ReportFormTestCase(TestCase):
    """Unit tests for the ReportForm."""

    def setUp(self):
        self.valid_data = {
            'reason': 'spam',
            'description': 'This content is spam.'
        }

    # ---------- Field presence ----------

    def test_form_has_required_fields(self):
        form = ReportForm()
        self.assertIn('reason', form.fields)
        self.assertIn('description', form.fields)

    # ---------- Validation ----------

    def test_valid_report_form(self):
        form = ReportForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_missing_reason(self):
        form = ReportForm(data={
            'reason': '',
            'description': 'Some description'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_rejects_missing_description(self):
        form = ReportForm(data={
            'reason': 'spam',
            'description': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_rejects_missing_reason_and_description(self):
        form = ReportForm(data={
            'reason': '',
            'description': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_accepts_long_description(self):
        form = ReportForm(data={
            'reason': 'offensive',
            'description': 'x' * 1000
        })
        self.assertTrue(form.is_valid())
