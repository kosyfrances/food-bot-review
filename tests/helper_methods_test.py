import os
import unittest
from config import Config


class HelperMethodsTest(unittest.TestCase):

    def test_that_config_week_is_only_A_or_B(self):
        """
        This test ensures that the only value set for 'WEEK'
        in the envvars is A or B.
        """
        config = Config()
        week_options = ['A', 'B']

        if os.path.exists('./rtmbot.conf'):
            config.load_yaml('rtmbot.conf')
            self.assertIn(config['WEEK'], week_options)
        else:
            config.load_os_environ_vars('FB__')
            self.assertIn(config['FB__WEEK'], week_options)
