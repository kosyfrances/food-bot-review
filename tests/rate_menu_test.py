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

    @patch.object(Helper, 'get_meal_time', return_value='07:45:00')
    @patch.object(Helper, 'check_rating_time', return_value=True)
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

    @patch.object(CustomSQL, 'query', return_value=[(0,)])
    def test_check_multiple_rating_returns_false_if_count_is_zero(self, *args):
        self.assertFalse(Helper.check_multiple_rating(self.user_id, 'breakfast'))

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    def test_check_multiple_rating_returns_true_if_count_greater_than_zero(self, *args):
        self.assertTrue(Helper.check_multiple_rating(self.user_id, 'breakfast'))

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
    @patch.object(Helper, 'check_multiple_rating', return_value=0)
    @patch.object(Helper, 'check_rating_time', return_value=True)
    def test_valid_rate_returns_correct_template(self, *args):
        buff = ['rate', 'breakfast', '2', '5']

        rate_context = Helper.get_rate_template_context(buff, self.user_id)

        self.assertEqual(rate_context, {'template': 'rating_response',
                                        'context': {}})
        CustomSQL.query.assert_called_with(
            'SELECT id FROM menu_table WHERE meal = (%s) AND day = (%s) AND week = (%s) AND option = (%s)', ('breakfast', 'monday', '1', '2'))

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    @patch.object(CustomSQL, 'command', return_value='command object')
    @patch.object(Helper, 'check_rating_time', return_value=True)
    @patch.object(Helper, 'get_day_of_week', return_value='monday')
    @patch.object(Helper, 'get_week_number', return_value='1')
    @patch.object(Helper, 'check_multiple_rating', return_value=1)
    def test_multiple_check_template_rendered_if_rate_count_is_greater_than_zero(self, *args):
        buff = ['rate', 'breakfast', '2', '5']

        rate_context = Helper.get_rate_template_context(buff, self.user_id)
        self.assertEqual(rate_context, {'template': 'multiple_rating',
                                        'context': {'meal': 'breakfast'}})

    @patch.object(CustomSQL, 'query', return_value=[(3L,)])
    @patch.object(CustomSQL, 'command', return_value='command object')
    @patch.object(Helper, 'get_day_of_week', return_value='monday')
    @patch.object(Helper, 'get_week_number', return_value='1')
    @patch.object(Helper, 'check_multiple_rating', return_value=0)
    @patch.object(Helper, 'check_rating_time', return_value=False)
    def test_rate_before_time_template_rendered_for_rating_before_meal_time(self, *args):
        buff = ['rate', 'breakfast', '2', '5']

        rate_context = Helper.get_rate_template_context(buff, self.user_id)
        self.assertEqual(rate_context, {'template': 'rate_before_time',
                                        'context': {'meal': 'breakfast'}})

    @patch.object(Helper, 'get_meal_time', return_value='07:45:00')
    def test_check_rating_time_for_breakfast(self, *args):
        self.assertTrue(Helper.check_rating_time('breakfast', '07:50:00'))
        self.assertFalse(Helper.check_rating_time('breakfast', '07:44:00'))

    @patch.object(Helper, 'get_meal_time', return_value='13:30:00')
    def test_check_rating_time_for_lunch(self, *args):
        self.assertFalse(Helper.check_rating_time('lunch', '13:29:00'))
        self.assertTrue(Helper.check_rating_time('breakfast', '13:30:01'))

