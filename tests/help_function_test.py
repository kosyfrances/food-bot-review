import unittest
from plugins.food_bot_plugin import Responses, outputs


class TestHelpFunction(unittest.TestCase):

    def test_help_returns_correct_string(self):
        Responses.show_help(u'D0CLHTW20')

        self.assertEqual(len(outputs), 1)
        self.assertEqual(type(outputs[0]), list)
        self.assertEqual(outputs[0][0], u'D0CLHTW20')
        self.assertEqual(outputs[0][1], Responses.help_text)
