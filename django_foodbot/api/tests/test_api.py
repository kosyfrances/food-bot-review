import json

from django.core.urlresolvers import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import Menu, Rating


class FoodBotApiTestCase(APITestCase):
    """Class defined to test foodbot api."""

    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(day='monday', food='rice',
                                        meal='lunch', option=1, week=1)
        self.Rating = Rating.objects.create(created_at='2015-11-04 06:42:20.5587',
                                            user_id='U0BT88BS', menu=self.menu,
                                            rate=3, comment='wonderful')


class TestMenu(FoodBotApiTestCase):
    """Test for menu endpoint."""

    def test_get_menu_list_when_menu_exist(self):
        url = reverse_lazy('menulist')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertDictEqual(json.loads(response.content)['results'][0],
                             {'id': 1, 'day': 'monday', 'food': 'rice',
                              'meal': 'lunch', 'option': 1, 'week': 1})


class TestRating(FoodBotApiTestCase):
    """Test for rating endpoint."""

    def test_get_rating_list(self):
        url = reverse_lazy('ratinglist')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))

    def test_get_weekly_ratings(self):
        url = reverse_lazy('weeklyratinglist')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))

    def test_post_ratings(self):
        url = reverse_lazy('addrating', kwargs={'id': 4})
        data = {'user_id': '1', 'rate': 5}
        response = self.client.post(url, data)
        self.assertTrue(status.is_success(response.status_code))
