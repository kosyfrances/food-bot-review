from rest_framework.test import APIClient
from django.core.urlresolvers import reverse_lazy
from rest_framework.test import APITestCase
from api.models import Menu, Rating


class FoodBotApiTestCase(APITestCase):

    '''Class defined to test foodbot api.'''
    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(day='monday', food='rice',
                                        meal='lunch', option=1, week=1)
        self.Rating = Rating.objects.create(created_at='2015-11-04 06:42:20.5587',
                                            user_id='U0BT88BS', menu=self.menu,
                                            rate=3, comment='wonderful')


class TestMenu(FoodBotApiTestCase):

    def test_get_menu_list(self):
        url = reverse_lazy('menulist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_rating_list(self):
        url = reverse_lazy('ratinglist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_weekly_ratings(self):
        url = reverse_lazy('weeklyratinglist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
