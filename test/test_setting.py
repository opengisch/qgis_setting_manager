import unittest

from my_settings import MySettings


class TestSetting(unittest.TestCase):

    def test_setting(self):
        my_settings = MySettings('test_plugin')
        self.assertEqual( my_settings.value('test_string'), 'default_str')




if __name__ == '__main__':
    unittest.main()