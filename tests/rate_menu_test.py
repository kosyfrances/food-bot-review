import unittest
from mock import patch
from plugins.food_bot_plugin import Helper
from custom_sql import CustomSQL


class TestRateMenu(unittest.TestCase):

    def test_check_meal_selected(self):
        self.assertTrue(Helper.check_meal_selected('breakfast'))
        self.assertTrue(Helper.check_meal_selected('lunch'))
        self.assertFalse(Helper.check_meal_selected('breakfas'))
        self.assertFalse(Helper.check_meal_selected('unch'))
        self.assertFalse(Helper.check_meal_selected(None))
        self.assertFalse(Helper.check_meal_selected(5))

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    def test_check_option_selected(self, *args):
        option_str = Helper.check_option_selected('k', 'tuesday', '2',
                                                  'breakfast')
        option_zero = Helper.check_option_selected('0', 'tuesday', '2',
                                                   'breakfast')
        option_higher = Helper.check_option_selected('4', 'tuesday', '2',
                                                     'breakfast')
        option_ok = Helper.check_option_selected('2', 'tuesday', '2',
                                                 'breakfast')

        self.assertEqual(option_str, {'bool': False, 'option': 3})
        self.assertEqual(option_zero, {'bool': False, 'option': 3})
        self.assertEqual(option_higher, {'bool': False, 'option': 3})
        self.assertEqual(option_ok, {'bool': True})

    def test_check_rating(self):
        self.assertTrue(Helper.check_rating('4'))
        self.assertFalse(Helper.check_rating('6'))
        self.assertFalse(Helper.check_rating('w'))
        self.assertFalse(Helper.check_rating('asdf'))

    @patch.object(Helper, 'get_day_of_week', return_value="saturday")
    def test_user_gets_weekend_rate_error_on_weekend(self, *args):
        buff = ['rate', 'breakfast', '2', '5']
        user_id = 'U0774N56J'
        rate_context = Helper.get_rate_template_context(buff, user_id)

        self.assertEqual(rate_context, {'template': 'weekend_rate_error', 'context': {}})

    def test_wrong_meal_selected_returns_correct_error_template(self):
        pass
