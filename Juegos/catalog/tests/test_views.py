from django.test import TestCase
from django.urls import reverse
from catalog.models import Game


class TopGameListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_games = 13

        for game_id in range(number_of_games):
            Game.objects.create(
                title=f'Test Game {game_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/games/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/game_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)

    def test_lists_all_authors(self):
        # Get fifth page and confirm it has (exactly) remaining 1 items
        response = self.client.get(reverse('games') + '?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['top_game_list']) == 1)