import unittest
from nose_parameterized import parameterized

from my_settings import MySettings
from .. import Scope






class TestSetting(unittest.TestCase):
    @parameterized.expand([
        (s_name, setting_['default']) for s_name, setting_ in MySettings().settings.iteritems()
    ])

    def test_setting(self, name, default):
        self.assertEqual( MySettings().value(name), default)


if __name__ == '__main__':
    unittest.main()