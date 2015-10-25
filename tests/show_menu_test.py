import unittest
from mock import patch
from plugins.food_bot_plugin import Response, Helper
from custom_sql import CustomSQL


class TestShowMenu(unittest.TestCase):

    def setUp(self):
        self.sorted_menu = [('cereal and bananas/boiled egg', 'breakfast', '1'),
                            ('apples and bananas', 'breakfast', '2'),
                            ('bread with and eggs', 'breakfast', '3'),
                            ('oats and moi-moi', 'breakfast', '4'),
                            ('macaroni with sauteed vegetables', 'lunch', '1'),
                            ('coconut rice and coleslaw', 'lunch', '2')]

        self.unsorted_menu = [('oats and moi-moi', 'breakfast', '4'),
                              ('macaroni with sauteed vegetables', 'lunch', '1'),
                              ('apples and bananas', 'breakfast', '2'),
                              ('bread with and eggs', 'breakfast', '3'),
                              ('coconut rice and coleslaw', 'lunch', '2'),
                              ('cereal and bananas/boiled egg', 'breakfast', '1')]

    def test_convert_menu_list_to_dict(self):
        expected_dict = {
            'breakfast': {
                '1': 'cereal and bananas/boiled egg',
                '2': 'apples and bananas',
                '3': 'bread with and eggs',
                '4': 'oats and moi-moi'
            },
            'lunch': {
                '1': 'macaroni with sauteed vegetables',
                '2': 'coconut rice and coleslaw'
            }
        }
        sorted_menu_dict = Helper.convert_menu_list_to_dict(self.sorted_menu)
        unsorted_menu_dict = Helper.convert_menu_list_to_dict(self.unsorted_menu)

        def compare_menu_dict(menu_dict1, menu_dict2):
            for meal_time in menu_dict1:
                self.assertIn(meal_time, menu_dict2)
                for meal in menu_dict1[meal_time]:
                    self.assertEqual(menu_dict1[meal_time][meal],
                                     menu_dict2[meal_time][meal])

        compare_menu_dict(sorted_menu_dict, expected_dict)
        compare_menu_dict(expected_dict, sorted_menu_dict)
        compare_menu_dict(unsorted_menu_dict, expected_dict)
        compare_menu_dict(expected_dict, unsorted_menu_dict)

    @patch.object(Helper, 'convert_menu_list_to_dict',
                  return_value="menu list as dict")
    @patch.object(CustomSQL, 'query', return_value="custom sql query")
    @patch.object(Helper, 'get_day_of_week', return_value="monday")
    @patch.object(Helper, 'get_week_number', return_value="1")
    def test_correct_template_name_and_context(self, *args):
        invalid_day_response_dict = Helper.get_menu_template_context(['menu',
                                                                       'asdf'])
        weekend_response_dict = Helper.get_menu_template_context(['menu',
                                                                   'saturday'])
        weekend_response_dict2 = Helper.get_menu_template_context(['menu',
                                                                    'SUNDAY'])
        weekday_response_dict = Helper.get_menu_template_context(['menu',
                                                                   'tuesday'])
        menu_response_dict = Helper.get_menu_template_context(['menu'])

        self.assertEqual(invalid_day_response_dict,
                         {'template': 'invalid_day_error', 'context': {}})
        self.assertEqual(weekend_response_dict,
                         {'template': 'weekend_meal_error', 'context': {}})
        self.assertEqual(weekend_response_dict2,
                         {'template': 'weekend_meal_error', 'context': {}})
        self.assertEqual(weekday_response_dict, {'template': 'menu_response',
                         'context': {'menu': "menu list as dict"}})
        self.assertEqual(menu_response_dict, {'template': 'menu_response',
                         'context': {'menu': "menu list as dict"}})

        CustomSQL.query.assert_called_with("SELECT food, meal, option FROM menu_table WHERE day = (%s) AND week = (%s)",("monday", '1'))
