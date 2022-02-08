from django.test import TestCase
from django.urls import reverse
from catalog.models import Category, Game

# Create your tests here.

"""
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
"""

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='Action')

    def test_name_label(self):
        cat = Category.objects.get(id=1)
        field_label = cat._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        cat = Category.objects.get(id=1)
        max_length = cat._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)


class GameModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Game.objects.create(title='Test Game')

    def test_get_absolute_url(self):
        game = Game.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(game.get_all_page_url(), '/catalog/game/1')