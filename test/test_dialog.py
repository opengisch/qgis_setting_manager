import unittest
import nose2
from nose_parameterized import parameterized
from qgis.testing import start_app
from my_settings import MySettings
from my_settings_dialog import MySettingsDialog


def params(settings):
    param = []
    for s_name, setting_ in settings.iteritems():
        for widget in setting_['widgets']:
            param.append((s_name, widget))
    return param


class TestDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    @parameterized.expand(params(MySettings().settings))
    def test_dialog(self, name, widget_class):
        setting_ = MySettings().settings[name]

        # set value
        MySettings().set_value(name, setting_['default'])


        dlg = MySettingsDialog(name, widget_class, True, False)
        dlg.show()

        # detect widget
        setting = dlg.setting(name)
        self.assertIsNotNone(setting.widget())


        # set value


        MySettings().set_value(name, setting_['new_value'])
        self.assertEqual(MySettings().value(name), setting_['new_value'])



if __name__ == '__main__':
    nose2.main()