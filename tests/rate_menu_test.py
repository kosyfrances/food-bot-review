import unittest
from mock import patch
from plugins.food_bot_plugin import Helper
from custom_sql import CustomSQL


class TestRateMenu(unittest.TestCase):

    def setUp(self):
        self.user_id = 'U0774N56J'

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

    @patch.object(Helper, 'get_day_of_week', return_value='saturday')
    @patch.object(Helper, 'get_week_number', return_value=2)
    def test_user_gets_weekend_rate_error_on_weekend(self, *args):
        buff = ['rate', 'breakfast', '2', '5']
        user_id = 'U0774N56J'
        rate_context = Helper.get_rate_template_context(buff, user_id)

        self.assertEqual(rate_context, {'template': 'weekend_rate_error',
                                        'context': {}})

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    @patch.object(Helper, 'get_day_of_week', return_value='wednesday')
    @patch.object(Helper, 'get_week_number', return_value=2)
    def test_wrong_meal_selected_returns_correct_error_template(self, *args):
        buff = ['rate', 'asdflkj', '2', '5']

        rate_context = Helper.get_rate_template_context(buff, self.user_id)

        self.assertEqual(rate_context, {'template': 'invalid_meal',
                                        'context': {}})

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    @patch.object(Helper, 'get_day_of_week', return_value='wednesday')
    @patch.object(Helper, 'get_week_number', return_value=2)
    def test_wrong_option_selected_returns_correct_error_template(self, *args):
        buff = ['rate', 'breakfast', '10', '5']

        rate_context = Helper.get_rate_template_context(buff, self.user_id)

        self.assertEqual(rate_context, {'context': {'option_count': 3},
                                        'template': 'invalid_option'})

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    @patch.object(Helper, 'get_day_of_week', return_value='wednesday')
    @patch.object(Helper, 'get_week_number', return_value=2)
    def test_invalid_rating_returns_correct_error_template(self, *args):
        negative_rate_buff = ['rate', 'breakfast', '2', '-1']
        zero_rate_buff = ['rate', 'breakfast', '2', '0']
        above_rate_buff = ['rate', 'breakfast', '2', '6']

        negative_rate_context = Helper.get_rate_template_context(
            negative_rate_buff, self.user_id)
        zero_rate_context = Helper.get_rate_template_context(
            zero_rate_buff, self.user_id)
        above_rate_context = Helper.get_rate_template_context(
            above_rate_buff, self.user_id)

        self.assertEqual(negative_rate_context, {'context': {},
                                                 'template': 'invalid_rating'})
        self.assertEqual(zero_rate_context, {'context': {},
                                             'template': 'invalid_rating'})
        self.assertEqual(above_rate_context, {'context': {},
                                              'template': 'invalid_rating'})

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    @patch.object(CustomSQL, 'command', return_value='command object')
    @patch.object(Helper, 'get_day_of_week', return_value='monday')
    @patch.object(Helper, 'get_week_number', return_value='1')
    def test_valid_rate_returns_correct_template(self, *args):
        buff = ['rate', 'breakfast', '2', '5']

        # import pdb; pdb.set_trace()
        rate_context = Helper.get_rate_template_context(buff, self.user_id)

        self.assertEqual(rate_context, {'template': 'rating_response',
                                        'context': {}})
        CustomSQL.query.assert_called_with(
            'SELECT id FROM menu_table WHERE meal = (%s) AND day = (%s) AND week = (%s) AND option = (%s)', ('breakfast', 'monday', '1', '2'))
