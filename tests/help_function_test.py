import unittest
from plugins import food_bot_plugin
from plugins.food_bot_plugin import Response


class TestHelpFunction(unittest.TestCase):

    def setUp(self):
        food_bot_plugin.outputs = []
        self.outputs = food_bot_plugin.outputs

    def test_help_returns_correct_string(self):
        Response.show_help(u'D0CLHTW20')

        self.assertEqual(len(self.outputs), 1)
        self.assertEqual(type(self.outputs[0]), list)
        self.assertEqual(self.outputs[0][0], u'D0CLHTW20')
        self.assertEqual(self.outputs[0][1], Response.help_text)

    def test_help_response_goes_to_correct_channel(self):
        Response.show_help(u'E0C5HTW21')
        Response.show_help(u'J0CMHTW21')

        self.assertEqual(self.outputs[0][0], u'E0C5HTW21')
        self.assertEqual(self.outputs[1][0], u'J0CMHTW21')
        self.assertEqual(len(self.outputs), 2)
