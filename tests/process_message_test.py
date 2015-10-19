import unittest
import mock
from plugins.food_bot_plugin import process_message


class TestProcessMessage(unittest.TestCase):

    def setUp(self):
        self.data = {}
        self.data['channel'] = u'D0CLHTW20'
        self.data['user'] = u'U0774N56J'

    @mock.patch('plugins.food_bot_plugin.Responses')
    def test_show_help_was_called(self, mock_response):
        data = self.data
        data['text'] = u'help'

        process_message(data)

        self.assertTrue(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.enter_comment.called)
        self.assertFalse(mock_response.get_average_ratings.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Responses')
    def test_show_menu_was_called(self, mock_response):
        data = self.data
        data['text'] = u'menu'

        process_message(data)

        self.assertTrue(mock_response.show_menu.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.enter_comment.called)
        self.assertFalse(mock_response.get_average_ratings.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Responses')
    def test_rate_was_called(self, mock_response):
        data = self.data
        data['text'] = u'rate'

        process_message(data)

        self.assertTrue(mock_response.rate.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.enter_comment.called)
        self.assertFalse(mock_response.get_average_ratings.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Responses')
    def test_comment_was_called(self, mock_response):
        data = self.data
        data['text'] = u'comment'

        process_message(data)

        self.assertTrue(mock_response.enter_comment.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.get_average_ratings.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Responses')
    def test_get_rating_was_called(self, mock_response):
        data = self.data
        data['text'] = u'get-rating'

        process_message(data)

        self.assertTrue(mock_response.get_average_ratings.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.enter_comment.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Responses')
    def test_show_error_was_called_with_wrong_command(self, mock_response):
        data = self.data
        data['text'] = u'asdf'

        process_message(data)

        self.assertTrue(mock_response.show_error.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.enter_comment.called)
        self.assertFalse(mock_response.get_average_ratings.called)
