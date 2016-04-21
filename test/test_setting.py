import unittest
from nose_parameterized import parameterized

from my_settings import MySettings
from .. import Scope






class TestSetting(unittest.TestCase):
    @parameterized.expand([ (s_name) for s_name in MySettings().settings.keys() ])
    def test_setting(self, name):
        setting_ = MySettings().settings[name]

        MySettings().remove(name)

        # default
        self.assertEqual( MySettings().value(name), setting_['default'])

        # set value
        MySettings().set_value(name, setting_['new_value'])
        self.assertEqual(MySettings().value(name), setting_['new_value'])




if __name__ == '__main__':
    unittest.main()