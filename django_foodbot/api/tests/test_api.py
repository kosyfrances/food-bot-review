import json
import mock
from datetime import datetime

from django.core.urlresolvers import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import Menu, Rating


class FoodBotApiTestCase(APITestCase):
    """Class defined to test foodbot api."""

    def setUp(self):
        self.client = APIClient()
        old_testtime = datetime(2016, 4, 20, 11, 11, 16, 398810)

        self.menu = Menu.objects.create(day='monday', food='rice', meal='lunch',
                                        option=1, week=1)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = old_testtime
            self.rating = Rating.objects.create(created_at=old_testtime,
                                                user_id='U0BT88BS', menu=self.menu,
                                                rate=3, comment='wonderful')


class TestMenu(FoodBotApiTestCase):
    """Test for menu endpoint."""

    def test_get_menu_list_when_menu_exist(self):
        url = reverse_lazy('menulist')
        response = self.client.get(url)
        expected_content = {'id': 1, 'day': 'monday', 'food': 'rice',
                            'meal': 'lunch', 'option': 1, 'week': 1}

        self.assertTrue(status.is_success(response.status_code))
        self.assertDictEqual(json.loads(response.content)['results'][0],
                             expected_content)

    def test_get_menu_list_when_no_menu_exist(self):
        Menu.objects.all().delete()
        url = reverse_lazy('menulist')
        response = self.client.get(url)

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(json.loads(response.content)['results'], [])


class TestRating(FoodBotApiTestCase):
    """Test for rating endpoint."""

    def test_get_all_rating_list_when_rating_exist(self):
        url = reverse_lazy('ratinglist')
        response = self.client.get(url)
        expected_content = {'id': 4, 'created_at': '2016-04-20T10:11:16.398810Z',
                            'user_id': 'U0BT88BS', 'rate': 3, 'comment': 'wonderful',
                            'menu': 4}

        self.assertTrue(status.is_success(response.status_code))
        self.assertDictEqual(json.loads(response.content)['results'][0],
                             expected_content)

    def test_no_weekly_ratings_is_returned_when_there_is_none_for_the_week(self):
        url = reverse_lazy('weeklyratinglist')
        response = self.client.get(url)

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(json.loads(response.content)['results'], [])

    def test_get_all_rating_list_when_no_rating_exist(self):
        Rating.objects.all().delete()
        url = reverse_lazy('ratinglist')
        response = self.client.get(url)

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(json.loads(response.content)['results'], [])

    def test_post_ratings(self):
        url = reverse_lazy('addrating', kwargs={'id': 6})
        data = {'user_id': '1', 'rate': 5}
        response = self.client.post(url, data)

        self.assertTrue(status.is_success(response.status_code))
