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

import qgis
import os 
import yaml
from qgis.testing import start_app, unittest
from qgis.core import QgsMessageLog, Qgis, QgsTolerance
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QDoubleSpinBox, QLineEdit, QSpinBox, QSlider, QComboBox, QListWidget
from qgis.gui import QgsCollapsibleGroupBox, QgsColorButton, QgsProjectionSelectionWidget
QColor.__repr__ = lambda color: 'QColor: {} a: {}'.format(color.name(), color.alpha())

import nose2

from .my_settings import MySettings
from .my_settings_dialog import MySettingsDialog

from .. import Scope, UpdateMode


# TODO: remaining tests:
# string with QgsMapLayerComboBox and QButtonGroup and also comboMode:data, QgsFileWidget
# stringlist with QGroupBox



class TestDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()
        
    def test_dialog(self):
        cur_dir = os.path.dirname(__file__)
        definition_file = os.path.join(cur_dir, 'setting_config.yaml')
        with open(definition_file, 'r') as f:
            definition = yaml.load(f.read())

        for setting_definition_name, setting_definition in definition['settings'].items():
            for scope in Scope:
                if 'scope' in setting_definition:
                    setting_scope = eval(setting_definition['scope'])
                    if setting_scope is not scope:
                        continue
                for widget_name, widget in setting_definition['widgets'].items():
                    setting_name = '{}_{}_{}'.format(setting_definition_name, scope.name, widget_name)
                    widget_class = eval(str(widget_name))
                    default_value = eval(str(setting_definition['default_value']))
                    new_value = eval(str(setting_definition['new_value']))
                    init_widget = widget['init_widget'] if widget and 'init_widget' in widget else None

                    print('testing {} in dialog accept mode'.format(widget_class))
                    yield self.check_dialog_accept_update, setting_name, widget_class, default_value, new_value, init_widget
                    print('testing {} in auto update mode'.format(widget_class))
                    yield self.check_dialog_auto_update, setting_name, widget_class, default_value, new_value, init_widget

    def check_dialog_accept_update(self, setting_name, widget_class, default_value, new_value, init_widget: str):

        print('check_dialog_accept_update')
        print('setting_name: {}'.format(setting_name))
        print('widget_class: {}'.format(widget_class))
        print('default_value: {}'.format(default_value))
        print('new_value: {}'.format(new_value))
        print('init_widget: {}'.format(init_widget))

        # this will reset to default with new call of MySettings within MySettingsDialog
        MySettings().remove(setting_name)

        print('current setting value: {}'.format(MySettings().value(setting_name)))

        # create dialog
        self.dlg = MySettingsDialog(setting_name, widget_class, UpdateMode.DialogAccept, init_widget)
        self.dlg.DEBUG = True
        self.dlg.show()

        # control that the widget is detected
        self.assertIn(setting_name, self.dlg.widget_list())

        # get widget
        setting_widget = self.dlg.setting_widget(setting_name)
        self.assertIsNotNone(setting_widget)

        # controls that widget is set to default
        print(setting_widget)
        self.assertEqual(setting_widget.widget_value(), default_value)

        # set value
        setting_widget.set_widget_value(new_value)

        # controls that widget has been update
        self.assertEqual(setting_widget.widget_value(), new_value)

        # accept dialog
        self.dlg.accept()

        # check setting has now new value
        self.assertEqual(MySettings().value(setting_name), new_value)
        self.dlg.close()

        # reset setting
        MySettings().remove(setting_name)

    def check_dialog_auto_update(self, setting_name, widget_class, default_value, new_value, init_widget: str):

        print('check_dialog_auto_update')

        # this will reset to default with new call of MySettings within MySettingsDialog
        MySettings().remove(setting_name)

        # test with direct update
        self.dlg = MySettingsDialog(setting_name, widget_class, UpdateMode.WidgetUpdate, init_widget)
        self.dlg.DEBUG = True
        self.dlg.show()

        # get widget
        setting_widget = self.dlg.setting_widget(setting_name)

        # controls that widget is set to default
        self.assertEqual(setting_widget.widget_value(), default_value)

        # set the widget with new value
        setting_widget.set_widget_value(new_value)

        # check that setting has been automatically updated
        self.assertEqual(MySettings().value(setting_name), new_value)

        self.dlg.close()

        # reset setting
        MySettings().remove(setting_name)


if __name__ == '__main__':
    nose2.main()
