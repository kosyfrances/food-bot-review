import unittest
from mock import patch
from plugins.food_bot_plugin import Response, Helper
from plugins import food_bot_plugin
from custom_sql import CustomSQL


class TestRateMenu(unittest.TestCase):

    def test_check_meal_selected(self):
        self.assertTrue(Helper.check_meal_selected('breakfast'))
        self.assertTrue(Helper.check_meal_selected('lunch'))
        self.assertFalse(Helper.check_meal_selected('breakfas'))
        self.assertFalse(Helper.check_meal_selected('unch'))
        self.assertFalse(Helper.check_meal_selected(None))
        self.assertFalse(Helper.check_meal_selected(5))

    # @patch('plugins.food_bot_plugin.get_day_of_week', return_value="saturday")
    # def test_user_gets_weekend_meal_error_on_weekend(self, *args):
    #     buff = ['rate', 'breakfast', '2', '5']
    #     rate_context = Response.get_rate_template_context(buff)
    #
    #     self.assertEqual(rate_context, {'template': 'weekend_meal_error', 'context': {}})
    #
    # def test_meal_selected_returns_correct_response(self):
    #     wrong_meal = food_bot_plugin.check_meal_selected('asdf', u'D0CLHTW20')
    #     breakfast = food_bot_plugin.check_meal_selected('breakfast', u'D0CLHTW20')
    #     lunch = food_bot_plugin.check_meal_selected('lunch', u'D0CLHTW20')
    #
    #     self.assertFalse(wrong_meal['bool'])
    #     self.assertEqual(wrong_meal['template'], 'invalid_meal')
    #
    #     self.assertTrue(breakfast['bool'])
    #     self.assertTrue(lunch['bool'])
