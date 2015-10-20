import unittest
from plugins.food_bot_plugin import Response


def tokenize_script(script):
    """Helper function to strip out new lines and tabs from scripts"""
    script_list = script.split('\n')
    return [s.strip() for s in script_list]


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
        sorted_menu_dict = Response.convert_menu_list_to_dict(self.sorted_menu)
        unsorted_menu_dict = Response.convert_menu_list_to_dict(self.unsorted_menu)

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

    def test_format_menu_response_returns_the_correct_string(self):
        menu = self.sorted_menu

        expected_string = """Here is the menu.```
                            Breakfast
                            option 1 : cereal and bananas/boiled egg
                            option 2 : apples and bananas
                            option 3 : bread with and eggs
                            option 4 : oats and moi-moi

                            Lunch
                            option 1 : macaroni with sauteed vegetables
                            option 2 : coconut rice and coleslaw
                            ```"""

        tokenize_expected_input = tokenize_script(Response.format_menu_response(menu))

        self.assertEqual(type(Response.format_menu_response(menu)), str)
        self.assertEqual(tokenize_expected_input, tokenize_script(expected_string))

    def test_format_menu_response_returns_correct_string_when_not_sorted(self):
        menu = self.unsorted_menu

        expected_string = """Here is the menu.```
                            Breakfast
                            option 1 : cereal and bananas/boiled egg
                            option 2 : apples and bananas
                            option 3 : bread with and eggs
                            option 4 : oats and moi-moi

                            Lunch
                            option 1 : macaroni with sauteed vegetables
                            option 2 : coconut rice and coleslaw
                            ```"""

        tokenize_expected_input = tokenize_script(Response.format_menu_response(menu))

        self.assertEqual(type(Response.format_menu_response(menu)), str)
        self.assertEqual(tokenize_expected_input, tokenize_script(expected_string))
