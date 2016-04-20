import unittest

from my_settings import MySettings
from .. import Scope

class TestSetting(unittest.TestCase):

    def test_setting(self):
        my_settings = MySettings()

        for setting_ in my_settings.settings:
            for scope_ in ('project', 'global'):
                # TODO python 3 use enum
                setting_name = '{}_{}'.format(setting_['name'], scope_)
                print(setting_name)
                self.assertEqual( my_settings.value(setting_name), setting_['default'])




if __name__ == '__main__':
    unittest.main()
