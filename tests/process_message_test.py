import unittest
import mock
from plugins.food_bot_plugin import process_message


class TestProcessMessage(unittest.TestCase):

    def setUp(self):
        self.data = {}
        self.data['channel'] = u'D0CLHTW20'
        self.data['user'] = u'U0774N56J'

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_show_help_was_called(self, mock_response):
        data = self.data
        data['text'] = u'help'

        process_message(data)

        self.assertTrue(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_show_menu_was_called(self, mock_response):
        data = self.data
        data['text'] = u'menu'

        process_message(data)

        self.assertTrue(mock_response.show_menu.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.rate.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_rate_was_called(self, mock_response):
        data = self.data
        data['text'] = u'rate breakfast 2 3'

        process_message(data)

        self.assertTrue(mock_response.rate.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.show_error.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_show_error_was_called_with_wrong_command(self, mock_response):
        data = self.data
        data['text'] = u'asdf'

        process_message(data)

        self.assertTrue(mock_response.show_error.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_bot_only_replies_to_direct_messages(self, mock_response):
        data = self.data
        data['channel'] = u'C0C1D62KA'

        process_message(data)

        self.assertFalse(mock_response.show_error.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_bot_does_not_respond_when_message_is_edited(self, mock_response):
        data = self.data
        data['subtype'] = u'message_changed'
        data.pop('user', None)

        process_message(data)

        self.assertFalse(mock_response.show_error.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_bot_does_not_respond_when_message_is_deleted(self, mock_response):
        data = self.data
        data['subtype'] = u'message_deleted'
        data.pop('user', None)

        process_message(data)

        self.assertFalse(mock_response.show_error.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)

    @mock.patch('plugins.food_bot_plugin.Response')
    def test_bot_does_not_respond_when_server_is_started(self, mock_response):
        data = self.data
        data['text'] = u'Here is the menu'
        data['reply_to'] = None

        process_message(data)

        self.assertFalse(mock_response.show_error.called)
        self.assertFalse(mock_response.show_help.called)
        self.assertFalse(mock_response.show_menu.called)
        self.assertFalse(mock_response.rate.called)
