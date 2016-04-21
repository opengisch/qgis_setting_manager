#-----------------------------------------------------------
#
# QGIS Setting Manager
# Copyright (C) 2016 Denis Rouzaud
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

import unittest
import nose2
from nose_parameterized import parameterized
from qgis.testing import start_app
from my_settings import MySettings
from my_settings_dialog import MySettingsDialog


# TODO: remaining tests:
# string with QgsMapLayerComboBox and QButtonGroup and also comboMode:data
# stringlist with QGroupBox


def params(settings):
    param = []
    for s_name, setting_ in settings.iteritems():
        for widget_class in setting_['widgets']:
            param.append(('{}_{}'.format(s_name, widget_class.__name__), s_name, widget_class))
    return param


class TestDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    @parameterized.expand(params(MySettings().settings_cfg))
    def test_dialog(self, test_name, name, widget_class):
        # reset to default value just in case
        setting_cfg = MySettings().settings_cfg[name]
        MySettings().set_value(name, setting_cfg['default'])

        # create dialog
        self.dlg = MySettingsDialog(name, widget_class, True, False)
        self.dlg.show()

        # control that the widget is detected
        self.assertIn(name, self.dlg.widget_list())

        # get widget
        setting_ = self.dlg.setting(name)
        widget = setting_.widget()
        self.assertIsNotNone(widget)

        # set value
        setting_.widget_set_method(setting_cfg['new_value'])

        # controls that widget has been update
        self.assertEqual(setting_.widget_get_method(), setting_cfg['new_value'])

        # accept dialog
        self.dlg.accept()

        # check setting has now new value
        self.assertEqual(MySettings().value(name), setting_cfg['new_value'])

if __name__ == '__main__':
    nose2.main()