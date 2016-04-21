import unittest
import nose2
from nose_parameterized import parameterized
from qgis.testing import start_app
from my_settings import MySettings
from my_settings_dialog import MySettingsDialog


class TestDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    @parameterized.expand([ (s_name) for s_name in MySettings().settings.keys() ])
    def test_dialog(self, name):
        setting_ = MySettings().settings[name]

        # set value
        MySettings().set_value(name, setting_['default'])

        for widget_class in setting_['widgets']:
            dlg = MySettingsDialog(name, widget_class, True, False)
            dlg.show()

            # set value
            print dlg.findChild(name).isChecked()

            MySettings().set_value(name, setting_['new_value'])
            self.assertEqual(MySettings().value(name), setting_['new_value'])



if __name__ == '__main__':
    nose2.main()