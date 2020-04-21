from django.test import TestCase
from ..models import Currency


class CurrencyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(name='CAD')

    def test_name_label(self):
        currency = Currency.objects.get(id=1)
        field_label = currency._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        currency = Currency.objects.get(id=1)
        max_length = currency._meta.get_field('name').max_length
        self.assertEquals(max_length, 3)

    def test_object_name_is_str(self):
        currency = Currency.objects.get(id=1)
        expected_object_name = currency.name
        self.assertEquals(expected_object_name, str(currency))