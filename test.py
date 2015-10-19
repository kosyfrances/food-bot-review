# To write tests here
import unittest
from plugins.food_bot_plugin import process_message


class TestProcessMessage(unittest.TestCase):

    def test_show_help(self):
        data = {}
        data['channel'] = u'D0CLHTW20'
        data['text'] = u'help'
        data['user'] = u'U0774N56J'

        show_help = process_message(data)
